from django.db import models

class Predio(models.Model):
    id_predio = models.AutoField(primary_key=True)
    nome_predio = models.CharField(max_length=100)

    class Meta:
        db_table = 'predio'

    def __str__(self):
        return self.nome_predio


class Localizacao(models.Model):
    id_localizacao = models.AutoField(primary_key=True)
    predio = models.ForeignKey(Predio, on_delete=models.SET_NULL, null=True)
    desc_localizacao = models.CharField(max_length=150)

    class Meta:
        db_table = 'localizacao'

    def __str__(self):
        return self.desc_localizacao