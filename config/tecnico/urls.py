from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tecnico.views import TecnicoViewSet

router = DefaultRouter()
router.register(r'tecnicos', TecnicoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]