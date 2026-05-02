from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.db import transaction

from usuario.models import Usuario
from grupo.models import Grupo
from grupo_usuario.models import GrupoUsuario


class UsuarioSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True)
    grupo = serializers.IntegerField(write_only=True)
    grupo_descricao = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id_usuario',
            'nome',
            'email',
            'senha',
            'grupo',
            'grupo_descricao'
        ]
        read_only_fields = ['id_usuario', 'grupo_descricao']

    def get_grupo_descricao(self, obj):
        vinculo = GrupoUsuario.objects.filter(usuario=obj).select_related('grupo').first()
        if vinculo:
            return vinculo.grupo.desc_grupo
        return None

    def validate_nome(self, value):
        if not value.strip():
            raise serializers.ValidationError("O nome é obrigatório.")
        return value

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Já existe um usuário com este e-mail.")
        return value

    def validate_grupo(self, value):
        if not Grupo.objects.filter(id_grupo=value).exists():
            raise serializers.ValidationError("Grupo informado não existe.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        senha = validated_data.pop('senha')
        id_grupo = validated_data.pop('grupo')

        grupo = Grupo.objects.get(id_grupo=id_grupo)

        usuario = Usuario.objects.create(
            nome=validated_data['nome'],
            email=validated_data['email'],
            senha_hash=make_password(senha)
        )

        GrupoUsuario.objects.create(
            usuario=usuario,
            grupo=grupo
        )

        return usuario

class UsuarioMeusDadosSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nome', 'email', 'senha']
        read_only_fields = ['id_usuario']

    def validate_nome(self, value):
        if not value.strip():
            raise serializers.ValidationError("O nome é obrigatório.")
        return value

    def validate_email(self, value):
        usuario_logado = self.instance

        if Usuario.objects.exclude(id_usuario=usuario_logado.id_usuario).filter(email=value).exists():
            raise serializers.ValidationError("Já existe um usuário com este e-mail.")

        return value

    def update(self, instance, validated_data):
        senha = validated_data.pop('senha', None)

        instance.nome = validated_data.get('nome', instance.nome)
        instance.email = validated_data.get('email', instance.email)

        if senha:
            instance.senha_hash = make_password(senha)

        instance.save()
        return instance