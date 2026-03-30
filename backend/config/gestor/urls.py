from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gestor.views import GestorViewSet

router = DefaultRouter()
router.register(r'gestores', GestorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]