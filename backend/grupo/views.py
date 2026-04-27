from rest_framework import generics
from grupo.models import Grupo
from grupo.serializers import GrupoSerializer
# Create your views here.

class GrupoListCreateView(generics.ListCreateAPIView):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer

class GrupoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer