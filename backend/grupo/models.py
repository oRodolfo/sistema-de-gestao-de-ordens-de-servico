from django.db import models

# Create your models here.

class Grupo(models.Model):
    id_grupo = models.BigAutoField(primary_key=True)
    desc_grupo = models.CharField(max_length=150)
    desc_permissao = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'grupo'

    def __str__(self):
        return self.desc_grupo