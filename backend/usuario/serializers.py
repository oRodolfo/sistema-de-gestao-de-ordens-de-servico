from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from usuario.models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nome', 'email', 'senha']
        read_only_fields = ['id_usuario']

    def create(self, validated_data):
        senha = validated_data.pop('senha')

        usuario = Usuario(
            nome=validated_data['nome'],
            email=validated_data['email'],
            senha_hash=make_password(senha)
        )

        usuario.save()
        return usuario