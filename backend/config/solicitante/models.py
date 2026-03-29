from django.db import models
from users.models import Usuario

class TipoSolicitante(models.Model):
    id_tipo_solicitante = models.AutoField(primary_key=True)
    desc_tipo_solicitante = models.CharField(max_length=150)

    def __str__(self):
        return self.desc_tipo_solicitante

class Solicitante(models.Model):
    id_solicitante = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    tipo_solicitante = models.ForeignKey(TipoSolicitante, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Solicitante - {self.usuario.nome}'