from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import Usuario, Grupo, GrupoUsuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['email', 'nome', 'is_active']
    search_fields = ['email', 'nome']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações pessoais', {'fields': ('nome',)}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'password1', 'password2'),
        }),
    )

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ['id_grupo', 'desc_grupo']

@admin.register(GrupoUsuario)
class GrupoUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'grupo']