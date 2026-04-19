from django.db import models
from orders.models.ordem_servico import OrdemServico
from users.models import Usuario

class Historico(models.Model):
    id_historico = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    data_registro = models.DateField(auto_now_add=True)
    desc_historico = models.CharField(max_length=150)

    class Meta:
        db_table = 'historico'

    def __str__(self):
        return f'Historico OS #{self.ordem_servico.id_ordem_servico}'