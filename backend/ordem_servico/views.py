from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from ordem_servico.models import OrdemServico
from ordem_servico.serializers import OrdemServicoSerializer, AtribuirTecnicoSerializer
from usuario.models import Usuario
from utils.responses import resposta_sucesso, resposta_erro
from utils.permissions import usuario_tem_grupo
from utils.historico import registrar_historico

# Create your views here.
# Views para a tabela ordem_servico, utilizando as permissões e regras de negócio definidas para cada tipo de usuário (solicitante, técnico, gestor e gerente).
class OrdemServicoListCreateView(generics.ListCreateAPIView):
    serializer_class = OrdemServicoSerializer
    permission_classes = (IsAuthenticated,)

    # Sobrescreve o método get_queryset para retornar as ordens de serviço de acordo com o tipo do usuário autenticado, aplicando as regras de acesso definidas para cada grupo (solicitante, técnico, gestor e gerente).
    def get_queryset(self):
        usuario = self.request.user

        if usuario_tem_grupo(usuario, "GERENTE"):
            return OrdemServico.objects.all().order_by('-dt_abertura')

        if usuario_tem_grupo(usuario, "GESTOR"):
            return OrdemServico.objects.filter(gestor=usuario).order_by('-dt_abertura')

        if usuario_tem_grupo(usuario, "TECNICO"):
            return OrdemServico.objects.filter(tecnico=usuario).order_by('-dt_abertura')

        return OrdemServico.objects.filter(solicitante=usuario).order_by('-dt_abertura')

    # Sobrescreve o método create para definir o solicitante como o usuário autenticado, definir o status como 'ABERTA' e a data de abertura como a data atual (quando a ordem-servico foi aberta). Também registra um histórico da abertura da ordem de serviço.
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            ordem_servico = serializer.save()

            registrar_historico(
                ordem_servico,
                request.user,
                f"Ordem de serviço aberta por {request.user.nome}. Status inicial: ABERTA."
            )

            return resposta_sucesso(
                "Ordem de serviço aberta com sucesso.",
                OrdemServicoSerializer(ordem_servico).data,
                status.HTTP_201_CREATED
            )

        return resposta_erro("Erro ao abrir ordem de serviço.", serializer.errors)

# View para recuperar, atualizar e deletar uma ordem de serviço específica, aplicando as regras de acesso e as validações necessárias para cada tipo de usuário (solicitante, técnico, gestor e gerente). O método update também registra históricos das alterações realizadas.
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

    # Sobrescreve o método retrieve para retornar uma ordem de serviço específica, aplicando as regras de acesso definidas para cada grupo (solicitante, técnico, gestor e gerente).
    def retrieve(self, request, *args, **kwargs):
        ordem_servico = self.get_object()
        return resposta_sucesso(
            "Ordem de serviço encontrada com sucesso.",
            self.get_serializer(ordem_servico).data
        )

    # Sobrescreve o método update para atualizar uma ordem de serviço específica, aplicando as regras de acesso e as validações necessárias para cada tipo de usuário (solicitante, técnico, gestor e gerente). O método também registra históricos das alterações realizadas.
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

                    registrar_historico(
                        ordem_servico,
                        usuario,
                        f"Dados atualizados por {usuario.nome}: {', '.join(campos_recebidos)}"
                    )

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

                    registrar_historico(
                        ordem_servico,
                        usuario,
                        f"Validação do solicitante: {status_anterior} -> {novo_status}"
                    )

                    return resposta_sucesso("Validação realizada", serializer.data)

                return resposta_erro("Erro na validação", serializer.errors)

            return resposta_erro("Operação não permitida.", None)

        # Regras para técnicos e gestores: só podem alterar o status da ordem de serviço, e apenas para os status permitidos para cada tipo de usuário. Além disso, técnicos só podem alterar ordens de serviço que estão atribuídas a eles, e gestores só podem alterar ordens de serviço que estão sob sua gestão.
        if usuario_tem_grupo(usuario, "TECNICO"):

            if ordem_servico.tecnico_id != usuario.id_usuario:
                return resposta_erro("Não é sua OS.", None)

            if campos_recebidos != {"status_ordem_servico"}:
                return resposta_erro("Técnico só altera status.", None)

            status_permitidos = [
                "EM_EXECUCAO",
                "AGUARDANDO_MATERIAL",
                "AGUARDANDO_TERCEIRO",
                "CONCLUIDA"
            ]

            if novo_status not in status_permitidos:
                return resposta_erro("Status inválido.", None)

            if novo_status == "EM_EXECUCAO":
                ocupado = OrdemServico.objects.filter(
                    tecnico=usuario,
                    status_ordem_servico="EM_EXECUCAO"
                ).exclude(id_ordem_servico=ordem_servico.id_ordem_servico).exists()

                if ocupado:
                    return resposta_erro("Já possui OS em execução.", None)

        # Regras para gestores: só podem alterar o status da ordem de serviço, e apenas para os status permitidos para gestores. Além disso, gestores só podem alterar ordens de serviço que estão sob sua gestão.
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
                registrar_historico(
                    ordem_servico,
                    usuario,
                    f"Status alterado: {status_anterior} -> {novo_status}"
                )

            return resposta_sucesso("Atualizado com sucesso", serializer.data)

        return resposta_erro("Erro ao atualizar", serializer.errors)

    # Sobrescreve o método destroy para cancelar uma ordem de serviço específica, aplicando as regras de acesso definidas para cada grupo (solicitante, técnico, gestor e gerente). Apenas ordens de serviço com status 'ABERTA' podem ser canceladas, e o método registra um histórico do cancelamento.
    def destroy(self, request, *args, **kwargs):
        ordem_servico = self.get_object()
        usuario = request.user

        if usuario_tem_grupo(usuario, "GERENTE") or ordem_servico.solicitante_id == usuario.id_usuario:

            if ordem_servico.status_ordem_servico != "ABERTA":
                return resposta_erro("Só pode cancelar OS aberta.", None)

            ordem_servico.status_ordem_servico = "CANCELADA"
            ordem_servico.dt_conclusao = timezone.now()
            ordem_servico.save()

            registrar_historico(
                ordem_servico,
                usuario,
                f"OS cancelada por {usuario.nome}"
            )

            return resposta_sucesso("Cancelada com sucesso", None)

        return resposta_erro("Sem permissão.", None)

# View para atribuir um técnico a uma ordem de serviço específica, aplicando as regras de acesso definidas para cada grupo (apenas gestores e gerentes podem acessar este endpoint). O método também registra um histórico da atribuição do técnico.
class OrdemServicoAtribuirTecnicoView(APIView):
    permission_classes = (IsAuthenticated)

    # Sobrescreve o método patch para atribuir um técnico a uma ordem de serviço específica, aplicando as regras de acesso definidas para cada grupo (apenas gestores e gerentes podem acessar este endpoint). O método também registra um histórico da atribuição do técnico.
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

        registrar_historico(
            os,
            request.user,
            f"Técnico atribuído: {tecnico.nome}"
        )

        return resposta_sucesso("Técnico atribuído", None)