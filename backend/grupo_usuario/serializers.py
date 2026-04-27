from rest_framework import serializers
from grupo_usuario.models import GrupoUsuario

class GrupoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoUsuario
        fields = '__all__'