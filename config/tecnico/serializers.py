from rest_framework import serializers
from tecnico.models import Tecnico

class TecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnico
        fields = ['id_tecnico', 'usuario', 'gestor', 'area_atuacao']