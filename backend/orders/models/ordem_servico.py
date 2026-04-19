from django.db import models
from orders.models.localizacao import Localizacao

class OrdemServico(models.Model):
    PRIORIDADE_CHOICES = [
        ('B', 'Baixa'),
        ('M', 'Média'),
        ('A', 'Alta'),
    ]

    STATUS_CHOICES = [
        ('A', 'Aberta'),
        ('E', 'Em andamento'),
        ('C', 'Concluída'),
        ('F', 'Fechada'),
    ]

    id_ordem_servico = models.AutoField(primary_key=True)
    localizacao = models.ForeignKey(Localizacao, on_delete=models.SET_NULL, null=True)
    prioridade_urgencia = models.CharField(max_length=1, choices=PRIORIDADE_CHOICES)
    status_ordem_servico = models.CharField(max_length=1, choices=STATUS_CHOICES)
    dt_abertura = models.DateField(auto_now_add=True)
    dt_conclusao = models.DateField(null=True, blank=True)
    descricao_servico = models.CharField(max_length=150)

    class Meta:
        db_table = 'ordem_servico'

    def __str__(self):
        return f'OS #{self.id_ordem_servico}'