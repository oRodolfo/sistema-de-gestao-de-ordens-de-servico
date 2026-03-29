from django.db import models
from orders.models.ordem_servico import OrdemServico

class GraficoIndicadores(models.Model):
    id_grafico = models.AutoField(primary_key=True)
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    desc_grafico = models.CharField(max_length=150)

    def __str__(self):
        return self.desc_grafico