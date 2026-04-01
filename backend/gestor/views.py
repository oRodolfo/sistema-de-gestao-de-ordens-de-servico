from rest_framework import viewsets
from gestor.models import Gestor
from gestor.serializers import GestorSerializer

class GestorViewSet(viewsets.ModelViewSet):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer