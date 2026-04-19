from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    nome = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    senha = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nome']

    def __str__(self):
        return self.nome


class Grupo(models.Model):
    id_grupo = models.AutoField(primary_key=True)
    desc_grupo = models.CharField(max_length=150)

    class Meta:
        db_table = 'grupo'

    def __str__(self):
        return self.desc_grupo


class GrupoUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'grupo_usuario'
        unique_together = (('usuario', 'grupo'),)

    def __str__(self):
        return f'{self.usuario.nome} - {self.grupo.desc_grupo}'