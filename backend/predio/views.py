from rest_framework import generics
from predio.models import Predio
from predio.serializers import PredioSerializer
# Create your views here.

class PredioListCreateView(generics.ListCreateAPIView):
    queryset = Predio.objects.all()
    serializer_class = PredioSerializer

class PredioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Predio.objects.all()
    serializer_class = PredioSerializer