from django.db import models

# Create your models here.
class Usuario(models.Model):
    id_usuario = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    email = models.CharField(max_length=150, unique=True)
    senha_hash = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'usuario'

    def __str__(self):
        return self.nome