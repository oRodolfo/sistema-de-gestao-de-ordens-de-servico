from rest_framework import viewsets
from gerente.models import Gerente
from gerente.serializers import GerenteSerializer

class GerenteViewSet(viewsets.ModelViewSet):
    queryset = Gerente.objects.all()
    serializer_class = GerenteSerializer