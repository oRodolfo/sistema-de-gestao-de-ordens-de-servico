from rest_framework import serializers
from grupo_usuario.models import GrupoUsuario
from usuario.models import Usuario
from grupo.models import Grupo

class GrupoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoUsuario
        fields = '__all__'
    
    def validate(self, data):
        id_usuario = data.get("id_usuario")
        id_grupo = data.get("id_grupo")

        if not Usuario.objects.filter(id_usuario=id_usuario).exists():
            raise serializers.ValidationError(
                {"id_usuario": "Usuário informado não existe."}
            )

        if not Grupo.objects.filter(id_grupo=id_grupo).exists():
            raise serializers.ValidationError(
                {"id_grupo": "Grupo informado não existe."}
            )

        if GrupoUsuario.objects.filter(id_usuario=id_usuario, id_grupo=id_grupo).exists():
            raise serializers.ValidationError(
                "Este usuário já está vinculado a este grupo."
            )

        return data