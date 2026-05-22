from django.db import models
from usuario.models import Usuario
from grupo.models import Grupo
# Create your models here.

# Modelo para a tabela "grupo_usuario", que representa a relação entre usuários e grupos
class GrupoUsuario(models.Model):

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')

    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, db_column='id_grupo')

    class Meta:
        managed = False
        db_table = 'grupo_usuario'
        unique_together = (('usuario', 'grupo'),)