from django.db import models
from tecnico.models import Tecnico
from gestor.models import Gestor
from orders.models.status_ordem import StatusOrdemServico
from orders.models.prioridade import Prioridade
from orders.models.localizacao import Localizacao
from orders.models.tipo_servico import TipoServico
from orders.models.validacao import Validacao

class OrdemServico(models.Model):
    id_ordem_servico = models.AutoField(primary_key=True)
    gestor = models.ForeignKey(Gestor, on_delete=models.SET_NULL, null=True)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.SET_NULL, null=True)
    prioridade = models.ForeignKey(Prioridade, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(StatusOrdemServico, on_delete=models.SET_NULL, null=True)
    localizacao = models.ForeignKey(Localizacao, on_delete=models.SET_NULL, null=True)
    tipo_servico = models.ForeignKey(TipoServico, on_delete=models.SET_NULL, null=True)
    validacao = models.ForeignKey(Validacao, on_delete=models.SET_NULL, null=True)
    dt_conclusao = models.DateField(null=True, blank=True)
    dt_abertura = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'OS #{self.id_ordem_servico}'