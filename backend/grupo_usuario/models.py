from django.db import models


class GrupoUsuario(models.Model):
    id_usuario = models.BigIntegerField(primary_key=True)
    id_grupo = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'grupo_usuario'
        unique_together = (('id_usuario', 'id_grupo'),)