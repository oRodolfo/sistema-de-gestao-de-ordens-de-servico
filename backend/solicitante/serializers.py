from rest_framework import serializers
from solicitante.models import Solicitante, TipoSolicitante

class TipoSolicitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoSolicitante
        fields = ['id_tipo_solicitante', 'desc_tipo_solicitante']

class SolicitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitante
        fields = ['id_solicitante', 'usuario', 'tipo_solicitante']