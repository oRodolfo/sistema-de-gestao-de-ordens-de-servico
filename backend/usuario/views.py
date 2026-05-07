from rest_framework import generics
from usuario.models import Usuario
from rest_framework import status
from usuario.serializers import UsuarioSerializer, UsuarioMeusDadosSerializer
from utils.responses import resposta_sucesso, resposta_erro
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsGerente
from rest_framework.views import APIView

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
            return resposta_sucesso(
                "Usuário cadastrado com sucesso.",
                UsuarioSerializer(usuario).data,
                status.HTTP_201_CREATED
            )

        return resposta_erro(
            "Erro ao cadastrar usuário.",
            serializer.errors
        )

# A view para recuperar, atualizar e deletar um usuário específico
# utilizando o serializer UsuarioSerializer e aplicando as permissões de IsAuthenticated e IsGerente para garantir que apenas usuários autenticados
# e com a permissão de gerente possam acessar essa funcionalidade.
class UsuarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # A view para recuperar, atualizar e deletar um usuário específico, utilizando o serializer UsuarioSerializer
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = (IsAuthenticated, IsGerente)

    # Limitamos os métodos HTTP permitidos para GET e DELETE, garantindo que essa view seja utilizada apenas para recuperar e deletar usuários, e não para atualizar.
    http_method_names = ['get', 'delete']

    # Sobrescrevemos os métodos retrieve e destroy para personalizar as respostas de sucesso
    # utilizando as funções resposta_sucesso e resposta_erro para garantir uma resposta consistente em toda a API.
    def retrieve(self, request, *args, **kwargs):
        usuario = self.get_object()
        serializer = self.get_serializer(usuario)

        return resposta_sucesso(
            "Usuário encontrado com sucesso.",
            serializer.data
        )

    def destroy(self, request, *args, **kwargs):
        usuario = self.get_object()
        usuario.delete()

        return resposta_sucesso(
            "Usuário removido com sucesso.",
            None,
            status.HTTP_204_NO_CONTENT
        )

# A view para permitir que o usuário autenticado visualize e atualize seus próprios dados
# utilizando o serializer UsuarioMeusDadosSerializer e aplicando a permissão de IsAuthenticated para garantir que apenas usuários autenticados possam acessar essa funcionalidade.
class UsuarioMeusDadosView(APIView):
    permission_classes = (IsAuthenticated,)
    
    # Sobrescrevemos os métodos get e patch para permitir que o usuário autenticado visualize e atualize seus próprios dados, 
    # utilizando as funções resposta_sucesso e resposta_erro para garantir uma resposta consistente em toda a API.
    def get(self, request):
        serializer = UsuarioSerializer(request.user)

        return resposta_sucesso(
            "Dados do usuário encontrados com sucesso.",
            serializer.data
        )

    # O método patch é utilizado para permitir que o usuário atualize seus próprios dados, 
    # utilizando o serializer UsuarioMeusDadosSerializer para validar e salvar as alterações, garantindo que a senha seja armazenada como hash se for fornecida.
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