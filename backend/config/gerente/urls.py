from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gerente.views import GerenteViewSet

router = DefaultRouter()
router.register(r'gerentes', GerenteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]