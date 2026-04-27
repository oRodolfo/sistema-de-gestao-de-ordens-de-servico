from rest_framework import generics
from ordem_servico.models import OrdemServico
from ordem_servico.serializers import OrdemServicoSerializer
# Create your views here.

class OrdemServicoListCreateView(generics.ListCreateAPIView):
    queryset = OrdemServico.objects.all()
    serializer_class = OrdemServicoSerializer

class OrdemServicoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrdemServico.objects.all()
    serializer_class = OrdemServicoSerializer