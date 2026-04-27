from rest_framework import generics
from historico.models import Historico
from historico.serializers import HistoricoSerializer
# Create your views here.

class HistoricoListCreateView(generics.ListCreateAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer

class HistoricoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer