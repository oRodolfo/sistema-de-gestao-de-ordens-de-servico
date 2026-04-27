from django.contrib import admin
from .models import GrupoUsuario

class GrupoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'id_grupo')
    search_fields = ('id_usuario', 'id_grupo')

admin.site.register(GrupoUsuario, GrupoUsuarioAdmin)