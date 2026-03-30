from django.db import models
from orders.models.ordem_servico import OrdemServico

class HistoricoAnterior(models.Model):
    id_historico_anterior = models.AutoField(primary_key=True)
    desc_historico = models.CharField(max_length=150)

    def __str__(self):
        return self.desc_historico

class Historico(models.Model):
    id_historico = models.AutoField(primary_key=True)
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    historico_anterior = models.OneToOneField(HistoricoAnterior, on_delete=models.SET_NULL, null=True, blank=True)
    data_registro = models.DateField(auto_now_add=True)
    descricao = models.CharField(max_length=150)

    def __str__(self):
        return f'Historico OS #{self.ordem_servico.id_ordem_servico}'