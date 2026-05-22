from rest_framework import serializers
from ativo.models import Ativo
from ativo.services import calcular_proxima_preventiva

class AtivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ativo
        fields = '__all__'
        read_only_fields = ['id_ativo', 'dt_proxima_preventiva']
    
    # Sobrescreve o método create para calcular a data da próxima manutenção preventiva com base na data da última manutenção e na periodicidade, garantindo que a data calculada seja um dia útil.
    def create(self, validated_data):
        dt_ultima = validated_data.get('dt_ultima_preventiva') # Obtém a data da última manutenção preventiva dos dados validados.
        periodicidade = validated_data.get('periodicidade_preventiva_dias') # Obtém a periodicidade em dias dos dados validados.

        # Se a data da última manutenção e a periodicidade forem fornecidas, calcula a data da próxima manutenção preventiva usando a função calcular_proxima_preventiva e adiciona essa data aos dados validados antes de criar o ativo.
        if dt_ultima and periodicidade:
            validated_data['dt_proxima_preventiva'] = (calcular_proxima_preventiva(dt_ultima, periodicidade))

        return super().create(validated_data)
    
    # Sobrescreve o método update para atualizar as informações do ativo, incluindo a data da próxima manutenção preventiva, garantindo que a data calculada seja um dia útil.
    def update(self, instance, validated_data):

        instance.localizacao = validated_data.get('localizacao', instance.localizacao)
        instance.codigo_patrimonial = validated_data.get('codigo_patrimonial', instance.codigo_patrimonial)
        instance.tipo_ativo = validated_data.get('tipo_ativo', instance.tipo_ativo)
        instance.marca = validated_data.get('marca', instance.marca)
        instance.modelo = validated_data.get('modelo', instance.modelo)
        instance.numero_serial = validated_data.get('numero_serial', instance.numero_serial)
        instance.periodicidade_preventiva_dias = validated_data.get('periodicidade_preventiva_dias', instance.periodicidade_preventiva_dias)
        instance.dt_ultima_preventiva = validated_data.get('dt_ultima_preventiva', instance.dt_ultima_preventiva)

        # Se a data da última manutenção e a periodicidade forem fornecidas, calcula a data da próxima manutenção preventiva usando a função calcular_proxima_preventiva e atualiza essa data no ativo antes de salvar as alterações.
        if instance.dt_ultima_preventiva and instance.periodicidade_preventiva_dias:
            instance.dt_proxima_preventiva = calcular_proxima_preventiva(instance.dt_ultima_preventiva, instance.periodicidade_preventiva_dias)

        instance.save()
        return instance