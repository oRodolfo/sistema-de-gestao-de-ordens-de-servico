from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UsuarioViewSet, LoginView, GrupoViewSet, GrupoUsuarioViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'grupos', GrupoViewSet)
router.register(r'grupo-usuario', GrupoUsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]