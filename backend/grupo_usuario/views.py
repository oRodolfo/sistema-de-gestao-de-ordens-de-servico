from rest_framework import generics
from grupo_usuario.models import GrupoUsuario
from grupo_usuario.serializers import GrupoUsuarioSerializer
# Create your views here.

class GrupoUsuarioListCreateView(generics.ListCreateAPIView):
    queryset = GrupoUsuario.objects.all()
    serializer_class = GrupoUsuarioSerializer

class GrupoUsuarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GrupoUsuario.objects.all()
    serializer_class = GrupoUsuarioSerializer