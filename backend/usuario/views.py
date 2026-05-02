from rest_framework import generics
from usuario.models import Usuario
from rest_framework import status
from usuario.serializers import UsuarioSerializer, UsuarioMeusDadosSerializer
from utils.responses import resposta_sucesso, resposta_erro
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsGerente
from rest_framework.views import APIView

class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, IsGerente]

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
    permission_classes = [IsAuthenticated, IsGerente]

    http_method_names = ['get', 'delete']

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

class UsuarioMeusDadosView(APIView):
    permission_classes = [IsAuthenticated]

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