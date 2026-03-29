from django.db import models
from users.models import Usuario

class Gestor(models.Model):
    id_gestor = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    area_atuacao = models.CharField(max_length=150)

    def __str__(self):
        return f'Gestor - {self.usuario.nome}'