from django.db import models
from orders.models.acoes import AprovarOrdemServico, TrocarOrdemServico, RecusarOrdemServico
from gestor.models import Gestor

class TipoAcaoOrdemServico(models.Model):
    id_tipo_acao_ordem_servico = models.AutoField(primary_key=True)
    aprovacao = models.ForeignKey(AprovarOrdemServico, on_delete=models.SET_NULL, null=True)
    recusa = models.ForeignKey(RecusarOrdemServico, on_delete=models.SET_NULL, null=True)
    troca = models.ForeignKey(TrocarOrdemServico, on_delete=models.SET_NULL, null=True)
    gestor = models.ForeignKey(Gestor, on_delete=models.SET_NULL, null=True)
    desc_tipo_acao = models.CharField(max_length=150)

    def __str__(self):
        return self.desc_tipo_acao