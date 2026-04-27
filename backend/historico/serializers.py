from rest_framework import serializers
from historico.models import Historico

class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = '__all__'