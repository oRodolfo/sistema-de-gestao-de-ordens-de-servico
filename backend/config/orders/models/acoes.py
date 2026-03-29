from django.db import models

class AprovarOrdemServico(models.Model):
    id_aprovacao = models.AutoField(primary_key=True)
    desc_aprovacao = models.CharField(max_length=150)

    def __str__(self):
        return self.desc_aprovacao

class RecusarOrdemServico(models.Model):
    id_recusa = models.AutoField(primary_key=True)
    desc_recusa = models.CharField(max_length=150)

    def __str__(self):
        return self.desc_recusa

class TrocarOrdemServico(models.Model):
    id_troca = models.AutoField(primary_key=True)
    desc_troca = models.CharField(max_length=150)

    def __str__(self):
        return self.desc_troca