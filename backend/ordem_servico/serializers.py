from rest_framework import serializers
from django.utils import timezone
from ordem_servico.models import OrdemServico

class AtribuirTecnicoSerializer(serializers.Serializer):
    tecnico = serializers.IntegerField()

class OrdemServicoSerializer(serializers.ModelSerializer):
    status_ordem_servico = serializers.CharField(required=False)
    localizacao_nome = serializers.SerializerMethodField()
    solicitante_nome = serializers.SerializerMethodField()
    tecnico_nome = serializers.SerializerMethodField()
    gestor_nome = serializers.SerializerMethodField()

    class Meta:
        model = OrdemServico
        fields = [
            'id_ordem_servico',
            'status_ordem_servico',
            'prioridade_urgencia',
            'dt_abertura',
            'dt_conclusao',
            'descricao_servico',
            'localizacao',
            'solicitante',
            'gestor',
            'tecnico',
            'localizacao_nome',
            'solicitante_nome',
            'tecnico_nome',
            'gestor_nome',
        ]
        read_only_fields = [
            'id_ordem_servico',
            'solicitante',
            'dt_abertura',
            'dt_conclusao'
        ]

    def get_localizacao_nome(self, obj):
        if obj.localizacao:
            return obj.localizacao.desc_localizacao
        return None

    def get_solicitante_nome(self, obj):
        if obj.solicitante:
            return obj.solicitante.nome
        return None

    def get_tecnico_nome(self, obj):
        if obj.tecnico:
            return obj.tecnico.nome
        return None

    def get_gestor_nome(self, obj):
        if obj.gestor:
            return obj.gestor.nome
        return None

    def validate_prioridade_urgencia(self, value):
        valores_validos = ['SIM', 'NAO']
        if value not in valores_validos:
            raise serializers.ValidationError("Valor inválido. Use: SIM ou NAO.")
        return value

    def validate_status_ordem_servico(self, value):
        status_validos = [
            'ABERTA', 'APROVADA', 'REPROVADA', 'EM_EXECUCAO',
            'AGUARDANDO_MATERIAL', 'AGUARDANDO_TERCEIRO',
            'CONCLUIDA', 'ENCERRADA', 'CANCELADA'
        ]
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
        validated_data.pop('status_ordem_servico', None)
        return OrdemServico.objects.create(
            solicitante=request.user,
            status_ordem_servico='ABERTA',
            dt_abertura=timezone.now(),
            **validated_data
        )
        
class AtribuirTecnicoSerializer(serializers.Serializer):
    tecnico = serializers.IntegerField()