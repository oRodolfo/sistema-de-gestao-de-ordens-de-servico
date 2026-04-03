from rest_framework import serializers
from users.models import Usuario
from users.enums import TipoUsuario

class UsuarioSerializer(serializers.ModelSerializer):
    tipo = serializers.ChoiceField(
        choices=[(t.value, t.name.capitalize()) for t in TipoUsuario]
    )

    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'tipo']
        extra_kwargs = {
            'senha': {'write_only': True}
        }

class CriarUsuarioSerializer(serializers.ModelSerializer):
    tipo = serializers.ChoiceField(
        choices=[(t.value, t.name.capitalize()) for t in TipoUsuario]
    )

    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'senha', 'tipo']
        extra_kwargs = {
            'senha': {'write_only': True}
        }

    def create(self, validated_data):
        usuario = Usuario.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['senha'],
            nome=validated_data['nome'],
            tipo=validated_data['tipo']
        )
        return usuario

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()