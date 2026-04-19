from rest_framework import serializers
from orders.models import OrdemServico, Localizacao, Predio, Historico

class PredioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predio
        fields = ['id_predio', 'nome_predio']

class LocalizacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localizacao
        fields = ['id_localizacao', 'predio', 'desc_localizacao']

class OrdemServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdemServico
        fields = [
            'id_ordem_servico', 'localizacao', 'prioridade_urgencia',
            'status_ordem_servico', 'dt_abertura', 'dt_conclusao',
            'descricao_servico'
        ]

class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = [
            'id_historico', 'usuario', 'ordem_servico',
            'data_registro', 'desc_historico'
        ]