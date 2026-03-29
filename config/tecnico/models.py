from django.db import models
from users.models import Usuario
from gestor.models import Gestor

class Tecnico(models.Model):
    id_tecnico = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    gestor = models.ForeignKey(Gestor, on_delete=models.SET_NULL, null=True)
    area_atuacao = models.CharField(max_length=150)

    def __str__(self):
        return f'Tecnico - {self.usuario.nome}'