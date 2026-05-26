from rest_framework import generics, status
from predio.models import Predio
from predio.serializers import PredioSerializer
from utils.responses import resposta_sucesso, resposta_erro
from rest_framework.permissions import IsAuthenticated
# Create your views here.

# View para listar e criar prédios. Utiliza a classe genérica ListCreateAPIView, que fornece implementações padrão para os métodos GET (listar) e POST (criar).
class PredioListCreateView(generics.ListCreateAPIView):
    queryset = Predio.objects.all()
    serializer_class = PredioSerializer
    #permission_classes = (IsAuthenticated,)

    # Sobrescreve o método create para fornecer uma resposta personalizada ao criar um prédio, incluindo mensagens de sucesso ou erro.
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            predio = serializer.save()
            return resposta_sucesso("Prédio cadastrado com sucesso.", PredioSerializer(predio).data, status.HTTP_201_CREATED)

        return resposta_erro("Erro ao cadastrar prédio.", serializer.errors)

# View para recuperar, atualizar e deletar um prédio específico. Utiliza a classe genérica RetrieveUpdateDestroyAPIView, que fornece implementações padrão para os métodos GET (recuperar), PUT/PATCH (atualizar) e DELETE (deletar).
class PredioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Predio.objects.all()
    serializer_class = PredioSerializer
    #permission_classes = (IsAuthenticated,)

    # Sobrescreve o método retrieve para fornecer uma resposta personalizada ao recuperar um prédio, incluindo mensagens de sucesso ou erro.
    def retrieve(self, request, *args, **kwargs):
        predio = self.get_object()
        return resposta_sucesso("Prédio encontrado com sucesso.", self.get_serializer(predio).data)

    # Sobrescreve o método update para fornecer uma resposta personalizada ao atualizar um prédio, incluindo mensagens de sucesso ou erro. Permite atualizações parciais (PATCH) ou completas (PUT).
    def update(self, request, *args, **kwargs):
        parcial = kwargs.pop("partial", False)
        predio = self.get_object()
        serializer = self.get_serializer(predio, data=request.data, partial=parcial)

        if serializer.is_valid():
            predio = serializer.save()
            return resposta_sucesso("Prédio atualizado com sucesso.", PredioSerializer(predio).data)

        return resposta_erro("Erro ao atualizar prédio.", serializer.errors)

    # Sobrescreve o método destroy para fornecer uma resposta personalizada ao deletar um prédio, incluindo mensagens de sucesso ou erro.
    def destroy(self, request, *args, **kwargs):
        predio = self.get_object()
        predio.delete()
        return resposta_sucesso("Prédio removido com sucesso.", None, status.HTTP_204_NO_CONTENT)