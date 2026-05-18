#atualizado todo quase ass zaia

from rest_framework import generics
from usuario.models import Usuario
from rest_framework import status
from usuario.serializers import UsuarioSerializer, UsuarioMeusDadosSerializer
from utils.responses import resposta_sucesso, resposta_erro
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsGerente
from rest_framework.views import APIView
from grupo_usuario.models import GrupoUsuario
from grupo.models import Grupo
from historico.models import Historico

class UsuarioListCreateView(generics.ListCreateAPIView):
    
    queryset = Usuario.objects.exclude(nome__startswith="[DESATIVADO]")
    serializer_class = UsuarioSerializer
    permission_classes = (IsAuthenticated, IsGerente)

    def create(self, request, *args, **kwargs):     
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            usuario = serializer.save()
            return resposta_sucesso(
                "Usuário cadastrado com sucesso.",
                UsuarioSerializer(usuario).data,
                status.HTTP_201_CREATED
            )

        return resposta_erro(
            "Erro ao cadastrar usuário.",
            serializer.errors
        )
class UsuarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = (IsAuthenticated, IsGerente)
    http_method_names = ['get', 'delete', 'put', 'patch']

    def retrieve(self, request, *args, **kwargs):
        usuario = self.get_object()
        serializer = self.get_serializer(usuario)

        return resposta_sucesso(
            "Usuário encontrado com sucesso.",
            serializer.data
        )

    def update(self, request, *args, **kwargs):
        usuario = self.get_object()
        
        novo_email = request.data.get('email')
        if novo_email and Usuario.objects.exclude(id_usuario=usuario.id_usuario).filter(email=novo_email).exists():
            return resposta_erro("Erro ao atualizar usuário.", {"email": ["Já existe um usuário com este e-mail."]})
            
        usuario.nome = request.data.get('nome', usuario.nome)
        usuario.email = request.data.get('email', usuario.email)
        usuario.save()
        
        id_grupo = request.data.get('grupo')
        if id_grupo:
            try:
                grupo_obj = Grupo.objects.get(pk=id_grupo)
                GrupoUsuario.objects.update_or_create(
                    usuario=usuario,
                    defaults={'grupo': grupo_obj}
                )
            except Grupo.DoesNotExist:
                pass
        
        return resposta_sucesso(
            "Usuário atualizado com sucesso.",
            UsuarioSerializer(usuario).data
        )

    def destroy(self, request, *args, **kwargs):
        usuario = self.get_object()
        
        # Soft delete por modificação de string: preserva a chave estrangeira nas OS,
        # mas remove o acesso ao e-mail e marca visualmente como inativo.
        usuario.nome = f"[DESATIVADO] {usuario.nome}"
        usuario.email = f"desativado_{usuario.id_usuario}_{usuario.email}"
        usuario.save()

        return resposta_sucesso(
            "Usuário removido com sucesso.",
            None,
            status.HTTP_200_OK
        )

class UsuarioMeusDadosView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        serializer = UsuarioSerializer(request.user)

        return resposta_sucesso(
            "Dados do usuário encontrados com sucesso.",
            serializer.data
        )

    def patch(self, request):
        serializer = UsuarioMeusDadosSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            usuario = serializer.save()

            return resposta_sucesso(
                "Dados atualizados com sucesso.",
                UsuarioMeusDadosSerializer(usuario).data
            )

        return resposta_erro(
            "Erro ao atualizar seus dados.",
            serializer.errors
        )