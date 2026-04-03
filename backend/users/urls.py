from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UsuarioViewSet, LoginView  

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),  
]