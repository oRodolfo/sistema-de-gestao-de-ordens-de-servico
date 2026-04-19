from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.views import (
    OrdemServicoViewSet,
    LocalizacaoViewSet,
    PredioViewSet,
    HistoricoViewSet,
)

router = DefaultRouter()
router.register(r'ordens', OrdemServicoViewSet)
router.register(r'localizacoes', LocalizacaoViewSet)
router.register(r'predios', PredioViewSet)
router.register(r'historicos', HistoricoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]