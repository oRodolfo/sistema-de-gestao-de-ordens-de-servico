from rest_framework import serializers
from orders.models import (
    OrdemServico, StatusOrdemServico, TipoServico,
    Prioridade, ClassificacaoPrioridade, Localizacao,
    Predio, Validacao, StatusValidacao, Historico,
    HistoricoAnterior, AprovarOrdemServico, RecusarOrdemServico,
    TrocarOrdemServico, TipoAcaoOrdemServico, GraficoIndicadores
)

class StatusOrdemServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusOrdemServico
        fields = ['id_status', 'desc_status_ordem_servico']

class TipoServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServico
        fields = ['id_tipo_servico', 'desc_tipo_servico']

class ClassificacaoPrioridadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassificacaoPrioridade
        fields = ['id_classificacao_prioridade', 'desc_classificacao_prioridade']

class PrioridadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prioridade
        fields = ['id_prioridade', 'gestor', 'classificacao_prioridade']

class PredioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predio
        fields = ['id_predio', 'nome_predio']

class LocalizacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localizacao
        fields = ['id_localizacao', 'predio', 'desc_localizacao']

class StatusValidacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusValidacao
        fields = ['id_status_validacao', 'desc_status_validacao']

class ValidacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Validacao
        fields = ['id_validacao', 'status_validacao', 'desc_validacao']

class AprovarOrdemServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AprovarOrdemServico
        fields = ['id_aprovacao', 'desc_aprovacao']

class RecusarOrdemServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecusarOrdemServico
        fields = ['id_recusa', 'desc_recusa']

class TrocarOrdemServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrocarOrdemServico
        fields = ['id_troca', 'desc_troca']

class TipoAcaoOrdemServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAcaoOrdemServico
        fields = ['id_tipo_acao_ordem_servico', 'aprovacao', 'recusa', 'troca', 'desc_tipo_acao']

class HistoricoAnteriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoAnterior
        fields = ['id_historico_anterior', 'desc_historico']

class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = ['id_historico', 'ordem_servico', 'historico_anterior', 'data_registro', 'descricao']

class GraficoIndicadoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraficoIndicadores
        fields = ['id_grafico', 'ordem_servico', 'desc_grafico']

class OrdemServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdemServico
        fields = [
            'id_ordem_servico', 'gestor', 'tecnico', 'prioridade',
            'status', 'localizacao', 'tipo_servico', 'validacao',
            'dt_conclusao', 'dt_abertura'
        ]