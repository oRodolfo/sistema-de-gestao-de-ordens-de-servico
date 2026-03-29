from django.db import models

class TipoServico(models.Model):
    id_tipo_servico = models.AutoField(primary_key=True)
    desc_tipo_servico = models.CharField(max_length=150)

    def __str__(self):
        return self.desc_tipo_servico