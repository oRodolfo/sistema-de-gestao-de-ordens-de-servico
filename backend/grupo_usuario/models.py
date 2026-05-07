from django.db import models
from usuario.models import Usuario
from grupo.models import Grupo
# Create your models here.

# Modelo para a tabela "grupo_usuario", que representa a relação entre usuários e grupos
class GrupoUsuario(models.Model):

    # Campos da tabela "grupo_usuario"
    usuario = models.ForeignKey( # Chave estrangeira para o modelo "Usuario", representando o usuário associado ao grupo
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        primary_key=True
    )

    grupo = models.ForeignKey( # Chave estrangeira para o modelo "Grupo", representando o grupo associado ao usuário
        Grupo,
        on_delete=models.CASCADE,
        db_column='id_grupo'
    )

    class Meta:
        managed = False # Indica que o Django não deve criar ou modificar a tabela no banco de dados
        db_table = 'grupo_usuario'
        unique_together = (('usuario', 'grupo'),) # Garante que a combinação de usuário e grupo seja única, evitando duplicatas

    def __str__(self):
        return f'{self.usuario} - {self.grupo}'