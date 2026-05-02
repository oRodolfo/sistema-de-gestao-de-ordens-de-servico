from rest_framework import serializers
from django.utils import timezone
from ordem_servico.models import OrdemServico


class OrdemServicoSerializer(serializers.ModelSerializer):
    status_ordem_servico = serializers.CharField(required=False)

    class Meta:
        model = OrdemServico
        fields = '__all__'
        read_only_fields = [
            'id_ordem_servico',
            'solicitante',
            'dt_abertura',
            'dt_conclusao'
        ]

    def validate_prioridade_urgencia(self, value):
        valores_validos = ['SIM', 'NAO']

        if value not in valores_validos:
            raise serializers.ValidationError("Valor inválido. Use: SIM ou NAO.")

        return value

    def validate_status_ordem_servico(self, value):
        status_validos = [
            'ABERTA',
            'APROVADA',
            'REPROVADA',
            'EM_EXECUCAO',
            'AGUARDANDO_MATERIAL',
            'AGUARDANDO_TERCEIRO',
            'CONCLUIDA',
            'ENCERRADA',
            'CANCELADA'
        ]

        if value not in status_validos:
            raise serializers.ValidationError("Status inválido para ordem de serviço.")

        return value

    def validate_descricao_servico(self, value):
        if not value.strip():
            raise serializers.ValidationError("A descrição da ordem de serviço é obrigatória.")

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