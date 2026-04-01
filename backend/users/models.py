from django.db import models
from django.contrib.auth.models import AbstractUser
from users.enums import TipoUsuario

class Usuario(AbstractUser):
    nome = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    senha = models.CharField(max_length=255)
    tipo = models.CharField(
        max_length=20,
        choices=[(t.value, t.name.capitalize()) for t in TipoUsuario],
        null=False,
        blank=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nome']

    def __str__(self):
        return f'{self.nome} - {self.tipo}'