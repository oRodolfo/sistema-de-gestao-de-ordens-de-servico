<template>
  <div class="p-8">

    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Minhas Ordens</h1>
      <p class="text-sm text-gray-500 mt-1">Ordens de serviço atribuídas a você</p>
    </div>

    <!-- Cards rápidos -->
    <div class="grid grid-cols-2 gap-4 mb-8 lg:grid-cols-4">
      <div v-for="card in cards" :key="card.label" class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
        <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">{{ card.label }}</p>
        <p class="text-2xl font-bold" :class="card.cor">{{ card.valor }}</p>
      </div>
    </div>

    <!-- Filtros -->
    <div class="flex gap-2 mb-6 flex-wrap">
      <button v-for="status in statusOpcoes" :key="status.value" @click="filtroStatus = status.value"
        :class="['px-4 py-2 rounded-lg text-sm font-semibold border transition-colors cursor-pointer',
          filtroStatus === status.value ? 'bg-blue-800 text-white border-blue-800' : 'bg-white text-gray-600 border-gray-300 hover:border-blue-400']">
        {{ status.label }}
        <span class="ml-1 text-xs opacity-75">({{ contarStatus(status.value) }})</span>
      </button>
    </div>

    <!-- Tabela -->
    <div class="bg-white rounded-lg shadow-sm overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">#</th>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Local</th>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Descrição</th>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Status</th>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Prioridade</th>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Abertura</th>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-if="ordensFiltradas.length === 0">
            <td colspan="7" class="px-6 py-12 text-center text-gray-400 text-sm">Nenhuma ordem encontrada.</td>
          </tr>
          <tr v-for="ordem in ordensFiltradas" :key="ordem.id_ordem_servico" class="hover:bg-gray-50">
            <td class="px-6 py-4 text-sm font-semibold text-gray-800">#{{ ordem.id_ordem_servico }}</td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ ordem.localizacao }}</td>
            <td class="px-6 py-4 text-sm text-gray-600 max-w-xs truncate">{{ ordem.descricao_servico }}</td>
            <td class="px-6 py-4">
              <span :class="['px-2 py-1 rounded-full text-xs font-semibold', corStatus(ordem.status_ordem_servico)]">
                {{ labelStatus(ordem.status_ordem_servico) }}
              </span>
            </td>
            <td class="px-6 py-4">
              <span :class="['px-2 py-1 rounded-full text-xs font-semibold', ordem.prioridade_urgencia === 'SIM' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-600']">
                {{ ordem.prioridade_urgencia === 'SIM' ? 'Urgente' : 'Normal' }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ formatarData(ordem.dt_abertura) }}</td>
            <td class="px-6 py-4 text-sm flex gap-2 flex-wrap">
              <button @click="abrirDetalhe(ordem)" class="text-blue-600 hover:text-blue-800 font-semibold cursor-pointer">Ver</button>
              <button v-if="ordem.status_ordem_servico === 'APROVADA'" @click="alterarStatus(ordem, 'EM_EXECUCAO')"
                class="text-yellow-600 hover:text-yellow-800 font-semibold cursor-pointer">Iniciar</button>
              <button v-if="ordem.status_ordem_servico === 'EM_EXECUCAO'" @click="abrirConcluir(ordem)"
                class="text-green-600 hover:text-green-800 font-semibold cursor-pointer">Concluir</button>
              <button v-if="ordem.status_ordem_servico === 'EM_EXECUCAO'" @click="alterarStatus(ordem, 'AGUARDANDO_MATERIAL')"
                class="text-orange-500 hover:text-orange-700 font-semibold cursor-pointer">Aguard. Material</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Detalhe -->
    <div v-if="mostrarModalDetalhe && ordemSelecionada" @click.self="mostrarModalDetalhe = false"
      class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
      <div class="bg-white rounded-xl p-8 w-full max-w-lg shadow-xl">
        <div class="flex justify-between items-start mb-6">
          <div>
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Ordem de Serviço</p>
            <h2 class="text-xl font-bold text-gray-800">#{{ ordemSelecionada.id_ordem_servico }}</h2>
          </div>
          <button @click="mostrarModalDetalhe = false" class="text-gray-400 hover:text-gray-600 cursor-pointer text-xl">✕</button>
        </div>
        <div class="flex gap-2 mb-6">
          <span :class="['px-3 py-1 rounded-full text-xs font-semibold', corStatus(ordemSelecionada.status_ordem_servico)]">
            {{ labelStatus(ordemSelecionada.status_ordem_servico) }}
          </span>
          <span :class="['px-3 py-1 rounded-full text-xs font-semibold', ordemSelecionada.prioridade_urgencia === 'SIM' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-600']">
            {{ ordemSelecionada.prioridade_urgencia === 'SIM' ? 'Urgente' : 'Normal' }}
          </span>
        </div>
        <div class="grid grid-cols-2 gap-4 mb-6">
          <div>
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Local</p>
            <p class="text-sm text-gray-800">{{ ordemSelecionada.localizacao }}</p>
          </div>
          <div>
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Data de Abertura</p>
            <p class="text-sm text-gray-800">{{ formatarData(ordemSelecionada.dt_abertura) }}</p>
          </div>
          <div>
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Solicitante</p>
            <p class="text-sm text-gray-800">{{ ordemSelecionada.solicitante }}</p>
          </div>
        </div>
        <div class="mb-6">
          <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Descrição</p>
          <p class="text-sm text-gray-700 bg-gray-50 rounded-lg p-4 leading-relaxed">{{ ordemSelecionada.descricao_servico }}</p>
        </div>
        <div class="flex justify-end gap-3">
          <button v-if="ordemSelecionada.status_ordem_servico === 'APROVADA'"
            @click="alterarStatus(ordemSelecionada, 'EM_EXECUCAO'); mostrarModalDetalhe = false"
            class="px-5 py-2 rounded-lg bg-yellow-500 text-white font-semibold hover:bg-yellow-600 cursor-pointer">Iniciar Execução</button>
          <button v-if="ordemSelecionada.status_ordem_servico === 'EM_EXECUCAO'"
            @click="mostrarModalDetalhe = false; abrirConcluir(ordemSelecionada)"
            class="px-5 py-2 rounded-lg bg-green-600 text-white font-semibold hover:bg-green-700 cursor-pointer">Concluir</button>
          <button @click="mostrarModalDetalhe = false"
            class="px-5 py-2 rounded-lg bg-blue-800 text-white font-semibold hover:bg-blue-600 cursor-pointer">Fechar</button>
        </div>
      </div>
    </div>

    <!-- Modal Concluir -->
    <div v-if="mostrarModalConcluir && ordemSelecionada" @click.self="mostrarModalConcluir = false"
      class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
      <div class="bg-white rounded-xl p-8 w-full max-w-md shadow-xl">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-bold text-gray-800">Concluir Ordem</h2>
          <button @click="mostrarModalConcluir = false" class="text-gray-400 hover:text-gray-600 cursor-pointer text-xl">✕</button>
        </div>
        <p class="text-sm text-gray-500 mb-4">
          Registre uma observação técnica sobre a conclusão da ordem <span class="font-semibold text-gray-800">#{{ ordemSelecionada.id_ordem_servico }}</span>
        </p>
        <div class="flex flex-col gap-2 mb-6">
          <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Observação Técnica</label>
          <textarea v-model="observacaoConclusao" rows="4" placeholder="Descreva o serviço realizado..."
            class="border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-blue-600 resize-none"></textarea>
        </div>
        <div class="flex gap-3">
          <button @click="mostrarModalConcluir = false"
            class="flex-1 py-3 rounded-lg border border-gray-300 text-gray-600 font-semibold hover:bg-gray-50 cursor-pointer">Cancelar</button>
          <button @click="confirmarConclusao"
            class="flex-1 py-3 rounded-lg bg-green-600 text-white font-semibold hover:bg-green-700 cursor-pointer">Confirmar Conclusão</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const filtroStatus = ref('')
const ordemSelecionada = ref<any>(null)
const mostrarModalDetalhe = ref(false)
const mostrarModalConcluir = ref(false)
const observacaoConclusao = ref('')

const statusOpcoes = [
  { value: '', label: 'Todas' },
  { value: 'APROVADA', label: 'Aprovadas' },
  { value: 'EM_EXECUCAO', label: 'Em Execução' },
  { value: 'AGUARDANDO_MATERIAL', label: 'Aguard. Material' },
  { value: 'CONCLUIDA', label: 'Concluídas' },
]

const ordens = ref([
  { id_ordem_servico: 2, localizacao: 'Biblioteca - Térreo', status_ordem_servico: 'EM_EXECUCAO', prioridade_urgencia: 'NAO', dt_abertura: '2026-04-27T08:15:00', descricao_servico: 'Troca de lâmpadas queimadas no corredor principal.', solicitante: 'Maria Souza' },
  { id_ordem_servico: 3, localizacao: 'Laboratório 3 - Bloco B', status_ordem_servico: 'AGUARDANDO_MATERIAL', prioridade_urgencia: 'SIM', dt_abertura: '2026-04-25T14:00:00', descricao_servico: 'Tomadas sem energia, necessário trocar disjuntor.', solicitante: 'Pedro Costa' },
  { id_ordem_servico: 6, localizacao: 'Bloco A - Sala 203', status_ordem_servico: 'APROVADA', prioridade_urgencia: 'SIM', dt_abertura: '2026-04-30T09:00:00', descricao_servico: 'Infiltração no teto causando goteiras.', solicitante: 'Carla Mendes' },
  { id_ordem_servico: 4, localizacao: 'Secretaria - Bloco C', status_ordem_servico: 'CONCLUIDA', prioridade_urgencia: 'NAO', dt_abertura: '2026-04-20T09:00:00', descricao_servico: 'Reparo na fechadura da porta principal.', solicitante: 'Ana Lima' },
])

const cards = computed(() => [
  { label: 'Total Atribuídas', valor: ordens.value.length, cor: 'text-blue-700' },
  { label: 'Em Execução', valor: ordens.value.filter(o => o.status_ordem_servico === 'EM_EXECUCAO').length, cor: 'text-yellow-500' },
  { label: 'Aguard. Material', valor: ordens.value.filter(o => o.status_ordem_servico === 'AGUARDANDO_MATERIAL').length, cor: 'text-orange-500' },
  { label: 'Concluídas', valor: ordens.value.filter(o => o.status_ordem_servico === 'CONCLUIDA').length, cor: 'text-green-600' },
])

const ordensFiltradas = computed(() => {
  if (!filtroStatus.value) return ordens.value
  return ordens.value.filter(o => o.status_ordem_servico === filtroStatus.value)
})

function contarStatus(status: string) {
  if (!status) return ordens.value.length
  return ordens.value.filter(o => o.status_ordem_servico === status).length
}

function formatarData(data: string) {
  return new Date(data).toLocaleDateString('pt-BR')
}

function abrirDetalhe(ordem: any) {
  ordemSelecionada.value = ordem
  mostrarModalDetalhe.value = true
}

function abrirConcluir(ordem: any) {
  ordemSelecionada.value = ordem
  observacaoConclusao.value = ''
  mostrarModalConcluir.value = true
}

function alterarStatus(ordem: any, novoStatus: string) {
  ordem.status_ordem_servico = novoStatus
}

function confirmarConclusao() {
  if (ordemSelecionada.value) {
    ordemSelecionada.value.status_ordem_servico = 'CONCLUIDA'
  }
  mostrarModalConcluir.value = false
  observacaoConclusao.value = ''
}

function corStatus(status: string) {
  const cores: Record<string, string> = {
    APROVADA: 'bg-green-100 text-green-700',
    EM_EXECUCAO: 'bg-yellow-100 text-yellow-700',
    AGUARDANDO_MATERIAL: 'bg-orange-100 text-orange-700',
    CONCLUIDA: 'bg-teal-100 text-teal-700',
  }
  return cores[status] || 'bg-gray-100 text-gray-600'
}

function labelStatus(status: string) {
  const labels: Record<string, string> = {
    APROVADA: 'Aprovada', EM_EXECUCAO: 'Em Execução',
    AGUARDANDO_MATERIAL: 'Aguard. Material', CONCLUIDA: 'Concluída',
  }
  return labels[status] || status
}
</script>