from rest_framework import generics
from usuario.models import Usuario
from rest_framework import status
from usuario.serializers import UsuarioSerializer, UsuarioMeusDadosSerializer
from utils.responses import resposta_sucesso, resposta_erro
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsGerente
from rest_framework.views import APIView
from grupo.models import Grupo
from grupo_usuario.models import GrupoUsuario
from django.contrib.auth.hashers import make_password

# Create your views here.
# As views abaixo utilizam os serializers definidos em serializers.py para criar, listar, atualizar e deletar usuários, 
# além de permitir que o usuário autenticado visualize e atualize seus próprios dados. 
# As permissões são configuradas para garantir que apenas usuários autenticados e com a permissão de gerente possam acessar as funcionalidades de gerenciamento de usuários.
class UsuarioListCreateView(generics.ListCreateAPIView):
    # A view para listar e criar usuários, utilizando o serializer UsuarioSerializer 
    # aplicando as permissões de IsAuthenticated e IsGerente para garantir que apenas usuários autenticados e com a permissão de gerente possam acessar essa funcionalidade.
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = (IsAuthenticated, IsGerente)

    # Limitamos os métodos HTTP permitidos para GET e POST, garantindo que essa view seja utilizada apenas para listar e criar usuários, e não para atualizar ou deletar.
    def create(self, request, *args, **kwargs):     
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            usuario = serializer.save()
            return resposta_sucesso("Usuário cadastrado com sucesso.", UsuarioSerializer(usuario).data, status.HTTP_201_CREATED)

        return resposta_erro("Erro ao cadastrar usuário.", serializer.errors)

# A view para recuperar, atualizar e deletar um usuário específico
# utilizando o serializer UsuarioSerializer e aplicando as permissões de IsAuthenticated e IsGerente para garantir que apenas usuários autenticados
# e com a permissão de gerente possam acessar essa funcionalidade.
class UsuarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # A view para recuperar, atualizar e deletar um usuário específico, utilizando o serializer UsuarioSerializer
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = (IsAuthenticated, IsGerente)

    # Limitamos os métodos HTTP permitidos para GET e DELETE, garantindo que essa view seja utilizada apenas para recuperar e deletar usuários, e não para atualizar.
    http_method_names = ('get', 'patch', 'delete')

    # Sobrescrevemos os métodos retrieve e destroy para personalizar as respostas de sucesso
    # utilizando as funções resposta_sucesso e resposta_erro para garantir uma resposta consistente em toda a API.
    def retrieve(self, request, *args, **kwargs):
        usuario = self.get_object()
        serializer = self.get_serializer(usuario)

        return resposta_sucesso("Usuário encontrado com sucesso.", serializer.data)
    
    def update(self, request, *args, **kwargs):
        usuario = self.get_object()

        novo_email = request.data.get('email')
        if novo_email and Usuario.objects.exclude(id_usuario=usuario.id_usuario).filter(email=novo_email).exists():
            return resposta_erro("Erro ao atualizar usuário.", {"email": ["Já existe um usuário com este e-mail."]})

        usuario.nome = request.data.get('nome', usuario.nome)
        usuario.email = request.data.get('email', usuario.email)

        nova_senha = request.data.get('senha')
        if nova_senha:
            usuario.senha_hash = make_password(nova_senha)

        usuario.save()

        id_grupo = request.data.get('grupo')
        if id_grupo:
            try:
                grupo_obj = Grupo.objects.get(pk=id_grupo)
                GrupoUsuario.objects.update_or_create(usuario=usuario, defaults={'grupo': grupo_obj})
            except Grupo.DoesNotExist:
                return resposta_erro("Erro ao atualizar usuário.", {"grupo": ["Grupo informado não existe."]})

        return resposta_sucesso("Usuário atualizado com sucesso.", UsuarioSerializer(usuario).data)

    # O método destroy é sobrescrito para personalizar a resposta de sucesso ao deletar um usuário, utilizando a função resposta_sucesso para garantir uma resposta consistente em toda a API.
    def destroy(self, request, *args, **kwargs):
        usuario = self.get_object()
        usuario.delete()

        return resposta_sucesso("Usuário removido com sucesso.", None, status.HTTP_200_OK)

# A view para permitir que o usuário autenticado visualize e atualize seus próprios dados
# utilizando o serializer UsuarioMeusDadosSerializer e aplicando a permissão de IsAuthenticated para garantir que apenas usuários autenticados possam acessar essa funcionalidade.
class UsuarioMeusDadosView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        serializer = UsuarioSerializer(request.user)

        return resposta_sucesso("Dados do usuário encontrados com sucesso.", serializer.data)

    def patch(self, request):
        serializer = UsuarioMeusDadosSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            usuario = serializer.save()

            return resposta_sucesso("Dados atualizados com sucesso.", UsuarioMeusDadosSerializer(usuario).data)

        return resposta_erro("Erro ao atualizar seus dados.", serializer.errors)