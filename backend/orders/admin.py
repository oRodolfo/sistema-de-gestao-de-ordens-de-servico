from django.contrib import admin
from orders.models.localizacao import Predio, Localizacao
from orders.models.ordem_servico import OrdemServico
from orders.models.historico import Historico

admin.site.register(Predio)
admin.site.register(Localizacao)
admin.site.register(OrdemServico)
admin.site.register(Historico)