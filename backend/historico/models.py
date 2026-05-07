from django.db import models
from usuario.models import Usuario
from ordem_servico.models import OrdemServico
# Create your models here.

# Modelo para representar o histórico de ordens de serviço
class Historico(models.Model):
    id_historico_ordem_servico = models.BigAutoField(primary_key=True)

    usuario = models.ForeignKey( # Relacionamento com o modelo Usuario
        Usuario,
        on_delete=models.DO_NOTHING,
        db_column='id_usuario'
    )

    ordem_servico = models.ForeignKey( # Relacionamento com o modelo OrdemServico
        OrdemServico,
        on_delete=models.CASCADE,
        db_column='id_ordem_servico'
    )

    data_registro = models.DateTimeField() # Campo para armazenar a data e hora do registro do histórico
    desc_historico = models.CharField(max_length=255) # Campo para armazenar uma descrição do histórico

    class Meta:
        managed = False # Indica que o Django não deve gerenciar a criação da tabela no banco de dados
        db_table = 'historico'

    def __str__(self):
        return f'Histórico OS #{self.ordem_servico.id_ordem_servico}'