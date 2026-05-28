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
from ativo.services import calcular_proxima_preventiva, criar_ou_atualizar_os_preventiva_para_ativo

class OrdemServicoListCreateView(generics.ListCreateAPIView):
    serializer_class = OrdemServicoSerializer

    # Remove IsAuthenticated fixo e define a regra por método
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny(),]
        return [IsAuthenticated()]

    #permission_classes = (IsAuthenticated,)

    # Sobrescreve o método get_queryset para retornar as ordens de serviço de acordo com o tipo do usuário autenticado, aplicando as regras de acesso definidas para cada grupo (solicitante, técnico, gestor e gerente).
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
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [IsAuthenticated(), IsGerenteOuGestorOuTecnico()]

        return [IsAuthenticated()]

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
        status_anterior = ordem_servico.status_ordem_servico

        serializer = self.get_serializer(ordem_servico, data=dados, partial=parcial)

        if serializer.is_valid():
            ordem_servico = serializer.save()

            if novo_status and novo_status != status_anterior:
                registrar_historico(
                    ordem_servico,
                    usuario,
                    f"Status alterado: {status_anterior} -> {novo_status}"
                )

            if (
                ordem_servico.tipo_manutencao == "PREVENTIVA"
                and novo_status in ["CONCLUIDA", "ENCERRADA"]
                and ordem_servico.ativo
            ):
                ordem_servico.dt_conclusao = timezone.now()
                ordem_servico.status_ordem_servico = "ENCERRADA"
                ordem_servico.save()

                ativo = ordem_servico.ativo
                ativo.dt_ultima_preventiva = timezone.now().date()

                if ativo.periodicidade_preventiva_dias:
                    ativo.dt_proxima_preventiva = calcular_proxima_preventiva(
                        ativo.dt_ultima_preventiva,
                        ativo.periodicidade_preventiva_dias,
                        ativo.localizacao,
                        ativo
                    )

                ativo.save()
                criar_ou_atualizar_os_preventiva_para_ativo(ativo)

                registrar_historico(
                    ordem_servico,
                    usuario,
                    f"Manutenção preventiva encerrada por {usuario.nome}. Próxima preventiva recalculada para {ativo.dt_proxima_preventiva}."
                )

                return resposta_sucesso(
                    "Manutenção preventiva encerrada com sucesso. Próxima preventiva gerada automaticamente.",
                    OrdemServicoSerializer(ordem_servico).data
                )

            return resposta_sucesso("Ordem de serviço atualizada com sucesso.", serializer.data)

        return resposta_erro("Erro ao atualizar ordem de serviço.", serializer.errors)

class OrdemServicoDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrdemServicoSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        ordem_servico = self.get_object()
        usuario = request.user

        if ordem_servico.status_ordem_servico in ["ENCERRADA", "CANCELADA"]:
            return resposta_erro("Esta ordem já está encerrada ou cancelada.", None)

        ordem_servico.status_ordem_servico = "CANCELADA"
        ordem_servico.dt_conclusao = timezone.now()
        ordem_servico.save()

        registrar_historico(
            ordem_servico,
            usuario,
            f"OS cancelada por {usuario.nome}"
        )

        return resposta_sucesso("Ordem de serviço cancelada com sucesso.", None)

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