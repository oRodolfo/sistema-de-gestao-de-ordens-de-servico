from django.db import models
from localizacao.models import Localizacao
# Create your models here.

class OrdemServico(models.Model):
    id_ordem_servico = models.BigAutoField(primary_key=True)
    localizacao = models.ForeignKey(
        Localizacao,
        on_delete=models.DO_NOTHING,
        db_column='id_localizacao'
    )
    prioridade_urgencia = models.CharField(max_length=20)
    status_ordem_servico = models.CharField(max_length=30)
    dt_abertura = models.DateTimeField()
    dt_conclusao = models.DateTimeField(null=True, blank=True)
    descricao_servico = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ordem_servico'

    def __str__(self):
        return f'OS #{self.id_ordem_servico}'