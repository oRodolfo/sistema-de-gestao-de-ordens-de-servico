from django.contrib import admin
from orders.models.acoes import AprovarOrdemServico, RecusarOrdemServico, TrocarOrdemServico
from orders.models.grafico import GraficoIndicadores
from orders.models.historico import HistoricoAnterior, Historico
from orders.models.localizacao import Predio, Localizacao
from orders.models.ordem_servico import OrdemServico
from orders.models.prioridade import ClassificacaoPrioridade, Prioridade
from orders.models.status_ordem import StatusOrdemServico
from orders.models.tipo_acao import TipoAcaoOrdemServico
from orders.models.tipo_servico import TipoServico
from orders.models.validacao import StatusValidacao, Validacao

admin.site.register(AprovarOrdemServico)
admin.site.register(RecusarOrdemServico)
admin.site.register(TrocarOrdemServico)
admin.site.register(GraficoIndicadores)
admin.site.register(HistoricoAnterior)
admin.site.register(Historico)
admin.site.register(Predio)
admin.site.register(Localizacao)
admin.site.register(OrdemServico)
admin.site.register(ClassificacaoPrioridade)
admin.site.register(Prioridade)
admin.site.register(StatusOrdemServico)
admin.site.register(TipoAcaoOrdemServico)
admin.site.register(TipoServico)
admin.site.register(StatusValidacao)
admin.site.register(Validacao)