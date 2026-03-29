from rest_framework import viewsets
from solicitante.models import Solicitante, TipoSolicitante
from solicitante.serializers import SolicitanteSerializer, TipoSolicitanteSerializer

class TipoSolicitanteViewSet(viewsets.ModelViewSet):
    queryset = TipoSolicitante.objects.all()
    serializer_class = TipoSolicitanteSerializer

class SolicitanteViewSet(viewsets.ModelViewSet):
    queryset = Solicitante.objects.all()
    serializer_class = SolicitanteSerializer