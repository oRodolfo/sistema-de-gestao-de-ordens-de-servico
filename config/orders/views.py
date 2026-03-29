from rest_framework import viewsets
from orders.models import (
    OrdemServico, StatusOrdemServico, TipoServico,
    Prioridade, ClassificacaoPrioridade, Localizacao,
    Predio, Validacao, StatusValidacao, Historico,
    HistoricoAnterior, AprovarOrdemServico, RecusarOrdemServico,
    TrocarOrdemServico, TipoAcaoOrdemServico, GraficoIndicadores
)
from orders.serializers import (
    OrdemServicoSerializer, StatusOrdemServicoSerializer, TipoServicoSerializer,
    PrioridadeSerializer, ClassificacaoPrioridadeSerializer, LocalizacaoSerializer,
    PredioSerializer, ValidacaoSerializer, StatusValidacaoSerializer, HistoricoSerializer,
    HistoricoAnteriorSerializer, AprovarOrdemServicoSerializer, RecusarOrdemServicoSerializer,
    TrocarOrdemServicoSerializer, TipoAcaoOrdemServicoSerializer, GraficoIndicadoresSerializer
)

class OrdemServicoViewSet(viewsets.ModelViewSet):
    queryset = OrdemServico.objects.all()
    serializer_class = OrdemServicoSerializer

class StatusOrdemServicoViewSet(viewsets.ModelViewSet):
    queryset = StatusOrdemServico.objects.all()
    serializer_class = StatusOrdemServicoSerializer

class TipoServicoViewSet(viewsets.ModelViewSet):
    queryset = TipoServico.objects.all()
    serializer_class = TipoServicoSerializer

class PrioridadeViewSet(viewsets.ModelViewSet):
    queryset = Prioridade.objects.all()
    serializer_class = PrioridadeSerializer

class ClassificacaoPrioridadeViewSet(viewsets.ModelViewSet):
    queryset = ClassificacaoPrioridade.objects.all()
    serializer_class = ClassificacaoPrioridadeSerializer

class LocalizacaoViewSet(viewsets.ModelViewSet):
    queryset = Localizacao.objects.all()
    serializer_class = LocalizacaoSerializer

class PredioViewSet(viewsets.ModelViewSet):
    queryset = Predio.objects.all()
    serializer_class = PredioSerializer

class ValidacaoViewSet(viewsets.ModelViewSet):
    queryset = Validacao.objects.all()
    serializer_class = ValidacaoSerializer

class StatusValidacaoViewSet(viewsets.ModelViewSet):
    queryset = StatusValidacao.objects.all()
    serializer_class = StatusValidacaoSerializer

class HistoricoViewSet(viewsets.ModelViewSet):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer

class HistoricoAnteriorViewSet(viewsets.ModelViewSet):
    queryset = HistoricoAnterior.objects.all()
    serializer_class = HistoricoAnteriorSerializer

class AprovarOrdemServicoViewSet(viewsets.ModelViewSet):
    queryset = AprovarOrdemServico.objects.all()
    serializer_class = AprovarOrdemServicoSerializer

class RecusarOrdemServicoViewSet(viewsets.ModelViewSet):
    queryset = RecusarOrdemServico.objects.all()
    serializer_class = RecusarOrdemServicoSerializer

class TrocarOrdemServicoViewSet(viewsets.ModelViewSet):
    queryset = TrocarOrdemServico.objects.all()
    serializer_class = TrocarOrdemServicoSerializer

class TipoAcaoOrdemServicoViewSet(viewsets.ModelViewSet):
    queryset = TipoAcaoOrdemServico.objects.all()
    serializer_class = TipoAcaoOrdemServicoSerializer

class GraficoIndicadoresViewSet(viewsets.ModelViewSet):
    queryset = GraficoIndicadores.objects.all()
    serializer_class = GraficoIndicadoresSerializer