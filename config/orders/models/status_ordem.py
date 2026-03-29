from django.db import models

class StatusOrdemServico(models.Model):
    id_status = models.AutoField(primary_key=True)
    desc_status_ordem_servico = models.CharField(max_length=150)

    def __str__(self):
        return self.desc_status_ordem_servico