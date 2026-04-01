from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.views import (
    OrdemServicoViewSet, StatusOrdemServicoViewSet, TipoServicoViewSet,
    PrioridadeViewSet, ClassificacaoPrioridadeViewSet, LocalizacaoViewSet,
    PredioViewSet, ValidacaoViewSet, StatusValidacaoViewSet, HistoricoViewSet,
    HistoricoAnteriorViewSet, AprovarOrdemServicoViewSet, RecusarOrdemServicoViewSet,
    TrocarOrdemServicoViewSet, TipoAcaoOrdemServicoViewSet, GraficoIndicadoresViewSet
)

router = DefaultRouter()
router.register(r'ordens', OrdemServicoViewSet)
router.register(r'status-ordem', StatusOrdemServicoViewSet)
router.register(r'tipos-servico', TipoServicoViewSet)
router.register(r'prioridades', PrioridadeViewSet)
router.register(r'classificacoes-prioridade', ClassificacaoPrioridadeViewSet)
router.register(r'localizacoes', LocalizacaoViewSet)
router.register(r'predios', PredioViewSet)
router.register(r'validacoes', ValidacaoViewSet)
router.register(r'status-validacao', StatusValidacaoViewSet)
router.register(r'historicos', HistoricoViewSet)
router.register(r'historicos-anteriores', HistoricoAnteriorViewSet)
router.register(r'aprovar-ordens', AprovarOrdemServicoViewSet)
router.register(r'recusar-ordens', RecusarOrdemServicoViewSet)
router.register(r'trocar-ordens', TrocarOrdemServicoViewSet)
router.register(r'tipos-acao', TipoAcaoOrdemServicoViewSet)
router.register(r'graficos', GraficoIndicadoresViewSet)

urlpatterns = [
    path('', include(router.urls)),
]