from rest_framework import serializers
from gestor.models import Gestor

class GestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gestor
        fields = ['id_gestor', 'usuario', 'area_atuacao']