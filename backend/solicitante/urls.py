from django.urls import path, include
from rest_framework.routers import DefaultRouter
from solicitante.views import SolicitanteViewSet, TipoSolicitanteViewSet

router = DefaultRouter()
router.register(r'solicitantes', SolicitanteViewSet)
router.register(r'tipos-solicitante', TipoSolicitanteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]