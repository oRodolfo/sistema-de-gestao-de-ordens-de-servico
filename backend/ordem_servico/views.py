from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response

from ordem_servico.models import OrdemServico
from ordem_servico.serializers import OrdemServicoSerializer, AtribuirTecnicoSerializer
from usuario.models import Usuario
from utils.responses import resposta_sucesso, resposta_erro
from utils.permissions import usuario_tem_grupo
from utils.historico import registrar_historico
from utils.permissions import IsGerenteOuGestorOuTecnico
from django.db.models import Count, Q, Avg, F

class OrdemServicoListCreateView(generics.ListCreateAPIView):
    serializer_class = OrdemServicoSerializer
    # Remove IsAuthenticated fixo e define a regra por método
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        usuario = self.request.user

        if usuario_tem_grupo(usuario, "GERENTE"):
            return OrdemServico.objects.all().order_by('-dt_abertura')

        if usuario_tem_grupo(usuario, "GESTOR"):
            from django.db.models import Q
            return OrdemServico.objects.filter(Q(gestor=usuario) | Q(status_ordem_servico='ABERTA')).order_by('-dt_abertura')

        if usuario_tem_grupo(usuario, "TECNICO"):
            return OrdemServico.objects.filter(tecnico=usuario).order_by('-dt_abertura')

        return OrdemServico.objects.filter(solicitante=usuario).order_by('-dt_abertura')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            ordem_servico = serializer.save()

            # Define as variáveis de verificação de autenticação
            usuario_autenticado = request.user if request.user and request.user.is_authenticated else None
            
            if usuario_autenticado:
                usuario_historico = usuario_autenticado
                nome_solicitante = request.user.nome
            else:
                # IMPORTANTE: Busca o primeiro usuário do banco para assinar o histórico do totem
                from usuario.models import Usuario
                usuario_historico = Usuario.objects.first() # Pega o administrador ou usuário ID 1 do banco
                nome_solicitante = "Usuário Anônimo"

            # Agora passamos um objeto de usuário válido que nunca será nulo
            registrar_historico(
                ordem_servico, 
                usuario_historico, 
                f"Ordem de serviço aberta por {nome_solicitante}. Status inicial: ABERTA."
            )

            return resposta_sucesso("Ordem de serviço aberta com sucesso.", OrdemServicoSerializer(ordem_servico).data, status.HTTP_201_CREATED)

        return resposta_erro("Erro ao abrir ordem de serviço.", serializer.errors)

class OrdemServicoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrdemServicoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        usuario = self.request.user

        if usuario_tem_grupo(usuario, "GERENTE"):
            return OrdemServico.objects.all()

        if usuario_tem_grupo(usuario, "GESTOR"):
            return OrdemServico.objects.filter(gestor=usuario)

        if usuario_tem_grupo(usuario, "TECNICO"):
            return OrdemServico.objects.filter(tecnico=usuario)

        return OrdemServico.objects.filter(solicitante=usuario)

    def retrieve(self, request, *args, **kwargs):
        ordem_servico = self.get_object()
        return resposta_sucesso("Ordem de serviço encontrada com sucesso.", self.get_serializer(ordem_servico).data)

    def update(self, request, *args, **kwargs):
        parcial = kwargs.pop("partial", False)
        ordem_servico = self.get_object()
        usuario = request.user

        if ordem_servico.status_ordem_servico in ["ENCERRADA", "CANCELADA"]:
            return resposta_erro("Esta ordem não pode mais ser alterada.", None)

        dados = request.data.copy()
        novo_status = dados.get("status_ordem_servico")
        campos_recebidos = set(dados.keys())

        campos_basicos = {"descricao_servico", "localizacao", "prioridade_urgencia"}
        usuario_eh_dono = ordem_servico.solicitante_id == usuario.id_usuario

        if usuario_eh_dono:

            if campos_recebidos.issubset(campos_basicos):

                if ordem_servico.status_ordem_servico in ["EM_EXECUCAO", "CONCLUIDA"]:
                    return resposta_erro("Não pode mais alterar dados após início da execução.", None)

                serializer = self.get_serializer(ordem_servico, data=dados, partial=True)

                if serializer.is_valid():
                    ordem_servico = serializer.save()

                    registrar_historico(ordem_servico, usuario, f"Dados updated por {usuario.nome}: {', '.join(campos_recebidos)}")

                    return resposta_sucesso("Atualizado com sucesso", serializer.data)

                return resposta_erro("Erro ao atualizar", serializer.errors)

            if campos_recebidos == {"status_ordem_servico"}:

                if ordem_servico.status_ordem_servico != "CONCLUIDA":
                    return resposta_erro("Só pode validar após CONCLUIDA.", None)

                if novo_status not in ["ENCERRADA", "REPROVADA"]:
                    return resposta_erro("Status inválido para validação.", None)

                status_anterior = ordem_servico.status_ordem_servico

                serializer = self.get_serializer(ordem_servico, data=dados, partial=True)

                if serializer.is_valid():
                    if novo_status == "ENCERRADA":
                        ordem_servico = serializer.save(dt_conclusao=timezone.now())
                    else:
                        ordem_servico = serializer.save()

                    registrar_historico(ordem_servico, usuario, f"Validação do solicitante: {status_anterior} -> {novo_status}")

                    return resposta_sucesso("Validação realizada", serializer.data)

                return resposta_erro("Erro na validação", serializer.errors)

            return resposta_erro("Operação não permitida.", None)

        if usuario_tem_grupo(usuario, "TECNICO"):

            if ordem_servico.tecnico_id != usuario.id_usuario:
                return resposta_erro("Não é sua OS.", None)

            if campos_recebidos != {"status_ordem_servico"}:
                return resposta_erro("Técnico só altera status.", None)

            status_permitidos = ["EM_EXECUCAO", "AGUARDANDO_MATERIAL", "AGUARDANDO_TERCEIRO", "CONCLUIDA"]

            if novo_status not in status_permitidos:
                return resposta_erro("Status inválido.", None)

            if novo_status == "EM_EXECUCAO":
                ocupado = OrdemServico.objects.filter(tecnico=usuario, status_ordem_servico="EM_EXECUCAO").exclude(id_ordem_servico=ordem_servico.id_ordem_servico).exists()

                if ocupado:
                    return resposta_erro("Já possui OS em execução.", None)

        elif usuario_tem_grupo(usuario, "GESTOR"):

            if ordem_servico.gestor_id != usuario.id_usuario:
                return resposta_erro("Não é sua OS.", None)

            if campos_recebidos != {"status_ordem_servico"}:
                return resposta_erro("Gestor só altera status.", None)

            if novo_status not in ["APROVADA", "REPROVADA"]:
                return resposta_erro("Status inválido.", None)

        elif usuario_tem_grupo(usuario, "GERENTE"):
            pass

        else:
            return resposta_erro("Sem permissão.", None)

        status_anterior = ordem_servico.status_ordem_servico

        serializer = self.get_serializer(ordem_servico, data=dados, partial=parcial)

        if serializer.is_valid():
            ordem_servico = serializer.save()

            if novo_status and novo_status != status_anterior:
                registrar_historico(ordem_servico, usuario, f"Status alterado: {status_anterior} -> {novo_status}")

            return resposta_sucesso("Atualizado com sucesso", serializer.data)

        return resposta_erro("Erro ao atualizar", serializer.errors)

class OrdemServicoDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrdemServicoSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        ordem_servico = self.get_object()
        usuario = request.user

        if usuario_tem_grupo(usuario, "GERENTE") or ordem_servico.solicitante_id == usuario.id_usuario:

            if ordem_servico.status_ordem_servico != "ABERTA":
                return resposta_erro("Só pode cancelar OS aberta.", None)

            ordem_servico.status_ordem_servico = "CANCELADA"
            ordem_servico.dt_conclusao = timezone.now()
            ordem_servico.save()

            registrar_historico(ordem_servico, usuario, f"OS cancelada por {usuario.nome}")

            return resposta_sucesso("Cancelada com sucesso", None)

        return resposta_erro("Sem permissão.", None)

class OrdemServicoAtribuirTecnicoView(APIView):
    permission_classes = (IsAuthenticated, IsGerenteOuGestorOuTecnico)

    def patch(self, request, pk):

        if not usuario_tem_grupo(request.user, "GESTOR") and not usuario_tem_grupo(request.user, "GERENTE"):
            return resposta_erro("Sem permissão.", None)

        try:
            os = OrdemServico.objects.get(pk=pk)
        except:
            return resposta_erro("OS não encontrada.", None)

        serializer = AtribuirTecnicoSerializer(data=request.data)

        if not serializer.is_valid():
            return resposta_erro("Erro.", serializer.errors)

        tecnico = Usuario.objects.get(id_usuario=serializer.validated_data["tecnico"])

        if not usuario_tem_grupo(tecnico, "TECNICO"):
            return resposta_erro("Usuário não é técnico.", None)

        os.tecnico = tecnico

        if os.gestor is None:
            os.gestor = request.user

        if os.status_ordem_servico == "ABERTA":
            os.status_ordem_servico = "APROVADA"

        os.save()

        registrar_historico(os, request.user, f"Técnico atribuído: {tecnico.nome}")

        return resposta_sucesso("Técnico atribuído", None)

class DashboardIndicadoresView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        usuario = request.user
        
        # 1. Filtro dinâmico: Gerente vê tudo, Gestor vê as dele + novas abertas
        if usuario_tem_grupo(usuario, "GERENTE"):
            base_query = OrdemServico.objects.all()
        else: # Considera como Gestor
            base_query = OrdemServico.objects.filter(Q(gestor=usuario) | Q(status_ordem_servico='ABERTA'))

        # 2. Contagem Geral e Agrupamento por Status usando a base filtrada
        total_ordens = base_query.count()
        status_counts = base_query.values('status_ordem_servico').annotate(total=Count('id_ordem_servico'))
        
        contagens = {
            'ABERTA': 0, 'APROVADA': 0, 'EM_EXECUCAO': 0,
            'AGUARDANDO_MATERIAL': 0, 'AGUARDANDO_TERCEIRO': 0,
            'CONCLUIDA': 0, 'CANCELADA': 0, 'REPROVADA': 0, 'ENCERRADA': 0,
        }
        
        for item in status_counts:
            st_nome = item['status_ordem_servico']
            if st_nome in contagens:
                contagens[st_nome] = item['total']

        # 3. Tempo Médio de Atendimento
        ordens_finalizadas = base_query.filter(
            dt_conclusao__isnull=False, 
            status_ordem_servico__in=['CONCLUIDA', 'ENCERRADA']
        )
        tempo_medio = "0d"
        if ordens_finalizadas.exists():
            try:
                dados_tempo = ordens_finalizadas.annotate(
                    duracao=F('dt_conclusao') - F('dt_abertura')
                ).aggregate(media_duracao=Avg('duracao'))
                
                duracao_media = dados_tempo['media_duracao']
                if duracao_media:
                    dias = duracao_media.days + (duracao_media.seconds / 86400)
                    tempo_medio = f"{dias:.1f}d"
            except Exception as e:
                print(f"Erro ao calcular tempo médio: {e}")

        # 4. Ranking de Técnicos (Protegido contra falha de related_name)
        tecnicos_data = []
        try:
            # Tenta buscar usando ordens_atribuidas que é o related_name definido no seu Usuario model
            ranking_tecnicos = (
                Usuario.objects.filter(cargo="TECNICO")
                .annotate(
                    total_os=Count('ordens_atribuidas'),
                    concluidas_os=Count('ordens_atribuidas', filter=Q(ordens_atribuidas__status_ordem_servico__in=['CONCLUIDA', 'ENCERRADA']))
                )
                .order_by('-total_os')[:4]
            )
            tecnicos_data = [
                {
                    'nome': t.nome,
                    'concluidas': t.concluidas_os,
                    'total': t.total_os
                } for t in ranking_tecnicos if t.total_os > 0
            ]
        except Exception as e:
            print(f"Erro no ranking de técnicos (tentando fallback): {e}")
            # Fallback seguro caso o name do relacionamento mude
            try:
                ranking_fallback = Usuario.objects.filter(cargo="TECNICO").annotate(
                    total_os=Count('ordemservico'),
                    concluidas_os=Count('ordemservico', filter=Q(ordemservico__status_ordem_servico__in=['CONCLUIDA', 'ENCERRADA']))
                ).order_by('-total_os')[:4]
                tecnicos_data = [{'nome': t.nome, 'concluidas': t.concluidas_os, 'total': t.total_os} for t in ranking_fallback if t.total_os > 0]
            except:
                pass

        # 5. Histórico Semanal das Últimas 6 Semanas (Usando a base filtrada)
        semanas_data = []
        agora = timezone.now()
        for i in range(5, -1, -1):
            fim_semana = agora - timedelta(weeks=i)
            inicio_semana = fim_semana - timedelta(days=7)
            
            qtd_semana = base_query.filter(
                status_ordem_servico__in=['CONCLUIDA', 'ENCERRADA'],
                dt_conclusao__range=(inicio_semana, fim_semana)
            ).count()
            
            semanas_data.append({
                'label': f'Sem {6 - i}',
                'valor': qtd_semana
            })

        # 6. Montagem Estruturada do Payload final
        dados_dashboard = {
            'totalOrdens': total_ordens,
            'abertas': contagens['ABERTA'],
            'emExecucao': contagens['EM_EXECUCAO'],
            'concluidas': contagens['CONCLUIDA'] + contagens['ENCERRADA'],
            'statusDetalhados': contagens,
            'rankingTecnicos': tecnicos_data,
            'pendencias': {
                'aguardando_aprovacao': contagens['ABERTA'],
                'aguardando_material': contagens['AGUARDANDO_MATERIAL'],
                'aguardando_terceiro': contagens['AGUARDANDO_TERCEIRO'],
                'sem_tecnico': base_query.filter(tecnico__isnull=True).count()
            },
            'semanas': semanas_data
        }

        return resposta_sucesso("Indicadores carregados com sucesso.", dados_dashboard)