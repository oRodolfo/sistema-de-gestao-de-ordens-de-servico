<template>
  <div class="p-8">

    <!-- Cabeçalho -->
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Ordens de Serviço</h1>
    </div>

    <!-- Filtros de status -->
    <div class="flex gap-2 mb-6 flex-wrap">
      <button
        v-for="status in statusOpcoes"
        :key="status.value"
        @click="filtroStatus = status.value"
        :class="[
          'px-4 py-2 rounded-lg text-sm font-semibold border transition-colors cursor-pointer',
          filtroStatus === status.value
            ? 'bg-blue-800 text-white border-blue-800'
            : 'bg-white text-gray-600 border-gray-300 hover:border-blue-400'
        ]"
      >
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
            <td colspan="7" class="px-6 py-12 text-center text-gray-400 text-sm">
              Nenhuma ordem encontrada para este filtro.
            </td>
          </tr>
          <tr
            v-for="ordem in ordensFiltradas"
            :key="ordem.id_ordem_servico"
            class="hover:bg-gray-50"
          >
            <td class="px-6 py-4 text-sm font-semibold text-gray-800">#{{ ordem.id_ordem_servico }}</td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ ordem.localizacao }}</td>
            <td class="px-6 py-4 text-sm text-gray-600 max-w-xs truncate">{{ ordem.descricao_servico }}</td>
            <td class="px-6 py-4 text-sm">
              <span :class="['px-2 py-1 rounded-full text-xs font-semibold', corStatus(ordem.status_ordem_servico)]">
                {{ labelStatus(ordem.status_ordem_servico) }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm">
              <span :class="['px-2 py-1 rounded-full text-xs font-semibold', ordem.prioridade_urgencia === 'SIM' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-600']">
                {{ ordem.prioridade_urgencia === 'SIM' ? 'Urgente' : 'Normal' }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-600">{{ formatarData(ordem.dt_abertura) }}</td>
            <td class="px-6 py-4 text-sm">
              <button
                @click="abrirDetalhe(ordem)"
                class="text-blue-600 hover:text-blue-800 font-semibold cursor-pointer"
              >
                Ver detalhes
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal de Detalhe -->
    <div
      v-if="mostrarModalDetalhe && ordemSelecionada"
      @click.self="mostrarModalDetalhe = false"
      class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center"
    >
      <div class="bg-white rounded-xl p-8 w-full max-w-lg shadow-xl">

        <!-- Cabeçalho -->
        <div class="flex justify-between items-start mb-6">
          <div>
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Ordem de Serviço</p>
            <h2 class="text-xl font-bold text-gray-800">#{{ ordemSelecionada.id_ordem_servico }}</h2>
          </div>
          <button @click="mostrarModalDetalhe = false" class="text-gray-400 hover:text-gray-600 cursor-pointer text-xl">✕</button>
        </div>

        <!-- Badges -->
        <div class="flex gap-2 mb-6">
          <span :class="['px-3 py-1 rounded-full text-xs font-semibold', corStatus(ordemSelecionada.status_ordem_servico)]">
            {{ labelStatus(ordemSelecionada.status_ordem_servico) }}
          </span>
          <span :class="['px-3 py-1 rounded-full text-xs font-semibold', ordemSelecionada.prioridade_urgencia === 'SIM' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-600']">
            {{ ordemSelecionada.prioridade_urgencia === 'SIM' ? 'Urgente' : 'Normal' }}
          </span>
        </div>

        <!-- Informações -->
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
          <div>
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Técnico</p>
            <p class="text-sm text-gray-800">{{ ordemSelecionada.tecnico || 'Não atribuído' }}</p>
          </div>
        </div>

        <!-- Descrição -->
        <div>
          <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Descrição do Serviço</p>
          <p class="text-sm text-gray-700 bg-gray-50 rounded-lg p-4 leading-relaxed">
            {{ ordemSelecionada.descricao_servico }}
          </p>
        </div>

        <!-- Fechar -->
        <div class="mt-6 flex justify-end">
          <button
            @click="mostrarModalDetalhe = false"
            class="px-6 py-2 rounded-lg bg-blue-800 text-white font-semibold hover:bg-blue-600 cursor-pointer"
          >
            Fechar
          </button>
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

const statusOpcoes = [
  { value: '', label: 'Todas' },
  { value: 'ABERTA', label: 'Abertas' },
  { value: 'APROVADA', label: 'Aprovadas' },
  { value: 'EM_EXECUCAO', label: 'Em Execução' },
  { value: 'AGUARDANDO_MATERIAL', label: 'Aguard. Material' },
  { value: 'AGUARDANDO_TERCEIRO', label: 'Aguard. Terceiro' },
  { value: 'CONCLUIDA', label: 'Concluídas' },
  { value: 'ENCERRADA', label: 'Encerradas' },
  { value: 'CANCELADA', label: 'Canceladas' },
]

const ordens = ref([
  {
    id_ordem_servico: 1,
    localizacao: 'Bloco A - Sala 101',
    status_ordem_servico: 'ABERTA',
    prioridade_urgencia: 'SIM',
    dt_abertura: '2026-04-28T10:30:00',
    descricao_servico: 'Ar condicionado com defeito, não resfria o ambiente.',
    solicitante: 'João Silva',
    tecnico: null,
  },
  {
    id_ordem_servico: 2,
    localizacao: 'Biblioteca - Térreo',
    status_ordem_servico: 'EM_EXECUCAO',
    prioridade_urgencia: 'NAO',
    dt_abertura: '2026-04-27T08:15:00',
    descricao_servico: 'Troca de lâmpadas queimadas no corredor principal.',
    solicitante: 'Maria Souza',
    tecnico: 'Carlos Técnico',
  },
  {
    id_ordem_servico: 3,
    localizacao: 'Laboratório 3 - Bloco B',
    status_ordem_servico: 'AGUARDANDO_MATERIAL',
    prioridade_urgencia: 'SIM',
    dt_abertura: '2026-04-25T14:00:00',
    descricao_servico: 'Tomadas sem energia, necessário trocar disjuntor.',
    solicitante: 'Pedro Costa',
    tecnico: 'Carlos Técnico',
  },
  {
    id_ordem_servico: 4,
    localizacao: 'Secretaria - Bloco C',
    status_ordem_servico: 'CONCLUIDA',
    prioridade_urgencia: 'NAO',
    dt_abertura: '2026-04-20T09:00:00',
    descricao_servico: 'Reparo na fechadura da porta principal.',
    solicitante: 'Ana Lima',
    tecnico: 'Roberto Técnico',
  },
  {
    id_ordem_servico: 5,
    localizacao: 'Cantina - Térreo',
    status_ordem_servico: 'APROVADA',
    prioridade_urgencia: 'NAO',
    dt_abertura: '2026-04-29T11:45:00',
    descricao_servico: 'Vazamento de água na pia da cozinha.',
    solicitante: 'Lucas Mendes',
    tecnico: null,
  },
  {
    id_ordem_servico: 6,
    localizacao: 'Bloco D - Corredor',
    status_ordem_servico: 'CANCELADA',
    prioridade_urgencia: 'NAO',
    dt_abertura: '2026-04-15T07:00:00',
    descricao_servico: 'Pintura do corredor solicitada erroneamente.',
    solicitante: 'Fernanda Lima',
    tecnico: null,
  },
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

function corStatus(status: string) {
  const cores: Record<string, string> = {
    ABERTA: 'bg-blue-100 text-blue-700',
    APROVADA: 'bg-green-100 text-green-700',
    EM_EXECUCAO: 'bg-yellow-100 text-yellow-700',
    AGUARDANDO_MATERIAL: 'bg-orange-100 text-orange-700',
    AGUARDANDO_TERCEIRO: 'bg-purple-100 text-purple-700',
    CONCLUIDA: 'bg-teal-100 text-teal-700',
    ENCERRADA: 'bg-gray-100 text-gray-700',
    CANCELADA: 'bg-red-100 text-red-700',
    REPROVADA: 'bg-red-200 text-red-800',
  }
  return cores[status] || 'bg-gray-100 text-gray-600'
}

function labelStatus(status: string) {
  const labels: Record<string, string> = {
    ABERTA: 'Aberta',
    APROVADA: 'Aprovada',
    EM_EXECUCAO: 'Em Execução',
    AGUARDANDO_MATERIAL: 'Aguard. Material',
    AGUARDANDO_TERCEIRO: 'Aguard. Terceiro',
    CONCLUIDA: 'Concluída',
    ENCERRADA: 'Encerrada',
    CANCELADA: 'Cancelada',
    REPROVADA: 'Reprovada',
  }
  return labels[status] || status
}
</script>