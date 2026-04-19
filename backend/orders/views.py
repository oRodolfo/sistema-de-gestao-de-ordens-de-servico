from rest_framework import viewsets
from orders.models import OrdemServico, Localizacao, Predio, Historico
from orders.serializers import (
    OrdemServicoSerializer, LocalizacaoSerializer,
    PredioSerializer, HistoricoSerializer
)

class OrdemServicoViewSet(viewsets.ModelViewSet):
    queryset = OrdemServico.objects.all()
    serializer_class = OrdemServicoSerializer

class LocalizacaoViewSet(viewsets.ModelViewSet):
    queryset = Localizacao.objects.all()
    serializer_class = LocalizacaoSerializer

class PredioViewSet(viewsets.ModelViewSet):
    queryset = Predio.objects.all()
    serializer_class = PredioSerializer

class HistoricoViewSet(viewsets.ModelViewSet):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer