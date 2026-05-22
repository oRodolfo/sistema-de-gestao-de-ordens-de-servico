from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.db import transaction

from usuario.models import Usuario
from grupo.models import Grupo
from grupo_usuario.models import GrupoUsuario

# Serializador para o modelo Usuario, utilizado para criar e representar os dados dos usuários na API.
class UsuarioSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True) # Campo de senha é write_only para garantir que a senha não seja exposta nas respostas da API.
    grupo = serializers.IntegerField(write_only=True) # Campo para receber o ID do grupo ao criar um usuário, é write_only porque não queremos expor o ID do grupo diretamente.
    grupo_descricao = serializers.SerializerMethodField(read_only=True) # Campo para retornar a descrição do grupo do usuário, é read_only porque é calculado a partir do relacionamento com o grupo.
 
    # Meta class para configurar o serializador, definindo o modelo e os campos que serão incluídos na serialização/deserialização.
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nome', 'email', 'senha', 'grupo', 'grupo_descricao']
        read_only_fields = ['id_usuario', 'grupo_descricao']

    # Método para obter a descrição do grupo do usuário, buscando o vínculo do usuário com o grupo e retornando a descrição do grupo.
    # O sistema não armazena o grupo diretamente no usuário, ele usa uma tabela de relacionamento grupo_usuario.
    def get_grupo_descricao(self, obj):
        vinculo = GrupoUsuario.objects.filter(usuario=obj).select_related('grupo').first()
        if vinculo:
            return vinculo.grupo.desc_grupo
        return None

    # Métodos de validação para os campos do serializador, garantindo que os dados sejam válidos antes de criar ou atualizar um usuário.
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

    # Método para criar um novo usuário, garantindo que a criação do usuário e a associação com o grupo sejam feitas todas juntas, ou seja, se algo der errado, nenhuma das operações será aplicada ao banco de dados.
    @transaction.atomic
    def create(self, validated_data):
        
        # Extraímos a senha e o ID do grupo dos dados validados, pois eles não fazem parte diretamente do modelo Usuario, mas são necessários para criar o usuário e associá-lo ao grupo.
        senha = validated_data.pop('senha')
        id_grupo = validated_data.pop('grupo')

        grupo = Grupo.objects.get(id_grupo=id_grupo)

        # Criamos o usuário com os dados validados e a senha hash, e depois criamos a associação do usuário com o grupo na tabela de relacionamento GrupoUsuario.
        usuario = Usuario.objects.create(nome=validated_data['nome'], email=validated_data['email'], senha_hash=make_password(senha))
        
        # Criamos a associação do usuário com o grupo na tabela de relacionamento GrupoUsuario, garantindo que o usuário seja vinculado ao grupo correto.
        GrupoUsuario.objects.create(usuario=usuario, grupo=grupo)

        return usuario

# Serializador para o endpoint "meus-dados", utilizado para permitir que o usuário autenticado visualize e atualize seus próprios dados.
class UsuarioMeusDadosSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, required=False) # Campo de senha é write_only e não é obrigatório para permitir atualizações sem alterar a senha.

    # Meta class para configurar o serializador, definindo o modelo e os campos que serão incluídos na serialização/deserialização, e indicando que o campo id_usuario é read_only.
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nome', 'email', 'senha']
        read_only_fields = ['id_usuario']

    # Métodos de validação para os campos do serializador, garantindo que os dados sejam válidos antes de atualizar o usuário.
    def validate_nome(self, value):
        if not value.strip():
            raise serializers.ValidationError("O nome é obrigatório.")
        return value

    def validate_email(self, value):
        usuario_logado = self.instance

        if Usuario.objects.exclude(id_usuario=usuario_logado.id_usuario).filter(email=value).exists():
            raise serializers.ValidationError("Já existe um usuário com este e-mail.")

        return value

    # Método para atualizar os dados do usuário, permitindo que o usuário atualize seu nome, email e senha (se fornecida), garantindo que a senha seja armazenada como hash.
    def update(self, instance, validated_data):
        senha = validated_data.pop('senha', None)

        instance.nome = validated_data.get('nome', instance.nome)
        instance.email = validated_data.get('email', instance.email)

        if senha:
            instance.senha_hash = make_password(senha)

        instance.save()
        return instance