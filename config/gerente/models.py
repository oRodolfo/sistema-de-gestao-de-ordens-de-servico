from django.db import models
from users.models import Usuario

class Gerente(models.Model):
    id_gerente = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f'Gerente - {self.usuario.nome}'