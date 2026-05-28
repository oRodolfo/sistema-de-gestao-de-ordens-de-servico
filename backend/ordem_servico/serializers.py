from rest_framework import serializers
from django.utils import timezone
from ordem_servico.models import OrdemServico


class OrdemServicoSerializer(serializers.ModelSerializer):
    status_ordem_servico = serializers.CharField(required=False)

    # Adicionados: Campos virtuais para retornar os nomes de texto para o Vue
    predio_nome = serializers.CharField(source='localizacao.predio.nome_predio', read_only=True, default="Totem")
    localizacao_nome = serializers.CharField(source='localizacao.desc_localizacao', read_only=True, default="") 
    solicitante_nome = serializers.CharField(source='solicitante.nome', read_only=True, default="Totem (Anônimo)")
    tecnico_nome = serializers.CharField(source='tecnico.nome', read_only=True, default="Não atribuído")

    class Meta:
        model = OrdemServico
        fields = '__all__'
        read_only_fields = ['id_ordem_servico', 'solicitante', 'dt_abertura', 'dt_conclusao']

    def validate_tipo_manutencao(self, value):
        valores_validos = ['CORRETIVA', 'PREVENTIVA']
        if value not in valores_validos:
            raise serializers.ValidationError("Tipo de manutenção inválido. Use: CORRETIVA ou PREVENTIVA.")
        return value

    def validate_categoria_manutencao(self, value):
        valores_validos = ['REFRIGERACAO', 'ELETRICA', 'GERAIS']
        if value not in valores_validos:
            raise serializers.ValidationError("Categoria de manutenção inválida. Use: REFRIGERACAO, ELETRICA ou GERAIS.")
        return value

    def validate_prioridade_urgencia(self, value):
        valores_validos = ['SIM', 'NAO']
        if value not in valores_validos:
            raise serializers.ValidationError("Valor inválido. Use: SIM ou NAO.")
        return value

    def validate_status_ordem_servico(self, value):
        status_validos = ['ABERTA', 'APROVADA', 'REPROVADA', 'EM_EXECUCAO', 'AGUARDANDO_MATERIAL', 'AGUARDANDO_TERCEIRO', 'CONCLUIDA', 'ENCERRADA', 'CANCELADA']
        if value not in status_validos:
            raise serializers.ValidationError("Status inválido.")
        return value

    def validate_descricao_servico(self, value):
        if not value.strip():
            raise serializers.ValidationError("A descrição é obrigatória.")
        if len(value.strip()) < 10:
            raise serializers.ValidationError("A descrição deve ter pelo menos 10 caracteres.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')

        # Remove chaves injetadas para garantir que o padrão inicial seja controlado pelo back-end
        validated_data.pop('status_ordem_servico', None)
        validated_data.pop('tipo_manutencao', None)

        # Trata a autenticação de forma segura para chamados logados vs chamados do Totem (anônimos)
        if request and request.user and request.user.is_authenticated:
            usuario_solicitante = request.user
        else:
            usuario_solicitante = None

        return OrdemServico.objects.create(
            solicitante=usuario_solicitante,
            tipo_manutencao='CORRETIVA',
            status_ordem_servico='ABERTA',
            dt_abertura=timezone.now(),
            **validated_data
        )


class AtribuirTecnicoSerializer(serializers.Serializer):
    tecnico = serializers.IntegerField()