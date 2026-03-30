from rest_framework import viewsets
from tecnico.models import Tecnico
from tecnico.serializers import TecnicoSerializer

class TecnicoViewSet(viewsets.ModelViewSet):
    queryset = Tecnico.objects.all()
    serializer_class = TecnicoSerializer