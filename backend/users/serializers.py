from rest_framework import serializers
from users.models import Usuario, Grupo, GrupoUsuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email']

class CriarUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'senha']
        extra_kwargs = {
            'senha': {'write_only': True}
        }

    def create(self, validated_data):
        usuario = Usuario.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['senha'],
            nome=validated_data['nome'],
        )
        return usuario

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ['id_grupo', 'desc_grupo']

class GrupoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoUsuario
        fields = ['id', 'usuario', 'grupo']