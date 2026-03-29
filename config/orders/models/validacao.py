from django.db import models

class StatusValidacao(models.Model):
    id_status_validacao = models.AutoField(primary_key=True)
    desc_status_validacao = models.CharField(max_length=150)

    def __str__(self):
        return self.desc_status_validacao

class Validacao(models.Model):
    id_validacao = models.AutoField(primary_key=True)
    status_validacao = models.ForeignKey(StatusValidacao, on_delete=models.SET_NULL, null=True)
    desc_validacao = models.CharField(max_length=150)

    def __str__(self):
        return self.desc_validacao