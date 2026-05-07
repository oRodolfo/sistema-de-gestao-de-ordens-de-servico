from django.db import models

# Create your models here.
# Criação do modelo Predio, que representa a tabela 'predio' no banco de dados.
class Predio(models.Model):
    id_predio = models.BigAutoField(primary_key=True)
    nome_predio = models.CharField(max_length=100)

    class Meta:
        managed = False # O Django não irá criar ou modificar a tabela 'predio' no banco de dados, pois ela já existe.
        db_table = 'predio'

    def __str__(self):
        return self.nome_predio