from rest_framework import generics
from localizacao.models import Localizacao
from localizacao.serializers import LocalizacaoSerializer
# Create your views here.

class LocalizacaoListCreateView(generics.ListCreateAPIView):
    queryset = Localizacao.objects.all()
    serializer_class = LocalizacaoSerializer

class LocalizacaoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Localizacao.objects.all()
    serializer_class = LocalizacaoSerializer