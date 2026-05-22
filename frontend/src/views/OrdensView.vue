<template>
  <div class="p-8">

    <!-- Cabeçalho -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-xl font-semibold text-gray-800">Ordens de Serviço</h1>
        <p class="text-sm text-gray-400 mt-0.5">Acompanhe e gerencie todas as ordens do sistema</p>
      </div>
      <span class="text-xs text-gray-400 bg-gray-100 px-3 py-1 rounded-full">
        {{ ordens.length }} registros
      </span>
    </div>

    <!-- Barra de filtros -->
    <div class="bg-white border border-gray-200 rounded-lg px-4 py-3 mb-4 flex gap-3 items-center">
      <span class="text-xs text-gray-400 font-medium uppercase tracking-wide shrink-0">Filtrar por</span>
      <select v-model="filtroStatus"
        class="text-sm border border-gray-200 rounded px-3 py-1.5 outline-none focus:border-blue-600 cursor-pointer">
        <option value="">Todos os status</option>
        <option v-for="s in statusOpcoes" :key="s.value" :value="s.value">{{ s.label }}</option>
      </select>
      <select v-model="filtroPrioridade"
        class="text-sm border border-gray-200 rounded px-3 py-1.5 outline-none focus:border-blue-600 cursor-pointer">
        <option value="">Todas as prioridades</option>
        <option value="SIM">Urgente</option>
        <option value="NAO">Normal</option>
      </select>
      <input v-model="busca" type="text" placeholder="Buscar por descrição ou local..."
        class="text-sm border border-gray-200 rounded px-3 py-1.5 outline-none focus:border-blue-600 flex-1" />
      <button v-if="filtroStatus || filtroPrioridade || busca"
        @click="filtroStatus = ''; filtroPrioridade = ''; busca = ''"
        class="text-xs text-gray-400 hover:text-gray-600 cursor-pointer whitespace-nowrap">
        Limpar filtros
      </button>
    </div>

    <!-- Tabela -->
    <div class="bg-white border border-gray-200 rounded-lg overflow-hidden">
      <table class="w-full">
        <thead>
          <tr class="bg-gray-50 border-b border-gray-200">
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide w-12">#</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide">Local</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide">Descrição</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide w-32">Status</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide w-24">Prioridade
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide w-28">Abertura</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide w-28">Conclusão</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide w-20">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-if="carregando">
            <td colspan="7" class="px-4 py-10 text-center text-sm text-gray-400">Carregando...</td>
          </tr>
          <tr v-else-if="ordensFiltradas.length === 0">
            <td colspan="7" class="px-4 py-10 text-center text-sm text-gray-400">Nenhuma ordem encontrada.</td>
          </tr>
          <tr v-for="ordem in ordensFiltradas" :key="ordem.id_ordem_servico" class="hover:bg-gray-50 transition-colors">
            <td class="px-4 py-3 text-sm text-gray-400 font-mono">#{{ ordem.id_ordem_servico }}</td>
            <td class="px-4 py-3 text-sm text-gray-700">{{ ordem.localizacao_nome || ordem.localizacao || '—' }}</td>
            <td class="px-4 py-3 text-sm text-gray-600 max-w-xs truncate">{{ ordem.descricao_servico }}</td>
            <td class="px-4 py-3">
              <span :class="['px-2 py-0.5 rounded text-xs font-medium', corStatus(ordem.status_ordem_servico)]">
                {{ labelStatus(ordem.status_ordem_servico) }}
              </span>
            </td>
            <td class="px-4 py-3">
              <span
                :class="['px-2 py-0.5 rounded text-xs font-medium', ordem.prioridade_urgencia === 'SIM' ? 'bg-red-50 text-red-600' : 'bg-gray-100 text-gray-500']">
                {{ ordem.prioridade_urgencia === 'SIM' ? 'Urgente' : 'Normal' }}
              </span>
            </td>
            <td class="px-4 py-3 text-sm text-gray-500">{{ formatarData(ordem.dt_abertura) }}</td>
            <td class="px-4 py-3 text-sm text-gray-500">{{ ordem.dt_conclusao ? formatarData(ordem.dt_conclusao) : '—' }}</td>
            <td class="px-4 py-3">
              <button @click="abrirDetalhe(ordem)"
                class="text-xs text-blue-700 hover:text-blue-900 font-medium cursor-pointer border border-blue-200 hover:border-blue-400 px-2 py-1 rounded transition-colors">
                Ver
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="px-4 py-3 border-t border-gray-100 bg-gray-50 flex items-center justify-between">
        <span class="text-xs text-gray-400">Exibindo {{ ordensFiltradas.length }} de {{ ordens.length }}
          registros</span>
      </div>
    </div>

    <!-- Modal de Detalhe -->
    <div v-if="mostrarModalDetalhe && ordemSelecionada" @click.self="mostrarModalDetalhe = false"
      class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
      <div class="bg-white rounded-lg w-full max-w-lg shadow-xl border border-gray-200 overflow-hidden">
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100 bg-gray-50">
          <div class="flex items-center gap-3">
            <span class="text-xs text-gray-400 font-mono">OS #{{ ordemSelecionada.id_ordem_servico }}</span>
            <span
              :class="['px-2 py-0.5 rounded text-xs font-medium', corStatus(ordemSelecionada.status_ordem_servico)]">
              {{ labelStatus(ordemSelecionada.status_ordem_servico) }}
            </span>
            <span
              :class="['px-2 py-0.5 rounded text-xs font-medium', ordemSelecionada.prioridade_urgencia === 'SIM' ? 'bg-red-50 text-red-600' : 'bg-gray-100 text-gray-500']">
              {{ ordemSelecionada.prioridade_urgencia === 'SIM' ? 'Urgente' : 'Normal' }}
            </span>
          </div>
          <button @click="mostrarModalDetalhe = false"
            class="text-gray-400 hover:text-gray-600 cursor-pointer text-lg leading-none">✕</button>
        </div>
        <div class="px-6 py-5">
          <table class="w-full text-sm mb-5">
            <tr class="border-b border-gray-100">
              <td class="py-2.5 text-xs text-gray-400 uppercase tracking-wide font-medium w-32">Local</td>
              <td class="py-2.5 text-gray-700">{{ ordemSelecionada.localizacao_nome || '—' }}</td>
            </tr>
            <tr class="border-b border-gray-100">
              <td class="py-2.5 text-xs text-gray-400 uppercase tracking-wide font-medium">Abertura</td>
              <td class="py-2.5 text-gray-700">{{ formatarData(ordemSelecionada.dt_abertura) }}</td>
            </tr>
            <tr class="border-b border-gray-100">
              <td class="py-2.5 text-xs text-gray-400 uppercase tracking-wide font-medium">Solicitante</td>
              <td class="py-2.5 text-gray-700">{{ ordemSelecionada.solicitante_nome || '—' }}</td>
            </tr>
            <tr class="border-b border-gray-100">
              <td class="py-2.5 text-xs text-gray-400 uppercase tracking-wide font-medium">Gestor</td>
              <td class="py-2.5 text-gray-700">{{ ordemSelecionada.gestor_nome || 'Não atribuído' }}</td>
            </tr>
            <tr>
              <td class="py-2.5 text-xs text-gray-400 uppercase tracking-wide font-medium">Técnico</td>
              <td class="py-2.5 text-gray-700">{{ ordemSelecionada.tecnico_nome || 'Não atribuído' }}</td>
            </tr>
            <tr v-if="ordemSelecionada.dt_conclusao" class="border-b border-gray-100">
              <td class="py-2.5 text-xs text-gray-400 uppercase tracking-wide font-medium">Conclusão</td>
              <td class="py-2.5 text-gray-700">{{ formatarData(ordemSelecionada.dt_conclusao) }}</td>
            </tr>
          </table>
          <div>
            <p class="text-xs text-gray-400 uppercase tracking-wide font-medium mb-2">Descrição</p>
            <p class="text-sm text-gray-700 bg-gray-50 border border-gray-100 rounded p-3 leading-relaxed">
              {{ ordemSelecionada.descricao_servico }}
            </p>
          </div>
        </div>
        <div class="flex justify-end gap-2 px-6 py-4 border-t border-gray-100">
          <button @click="mostrarModalDetalhe = false"
            class="px-4 py-2 text-sm rounded border border-gray-300 text-gray-600 hover:bg-gray-50 cursor-pointer">
            Fechar
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'

const filtroStatus = ref('')
const filtroPrioridade = ref('')
const busca = ref('')
const ordemSelecionada = ref<any>(null)
const mostrarModalDetalhe = ref(false)
const carregando = ref(false)
const ordens = ref<any[]>([])

const statusOpcoes = [
  { value: 'ABERTA', label: 'Aberta' },
  { value: 'APROVADA', label: 'Aprovada' },
  { value: 'EM_EXECUCAO', label: 'Em Execução' },
  { value: 'AGUARDANDO_MATERIAL', label: 'Ag. Material' },
  { value: 'AGUARDANDO_TERCEIRO', label: 'Ag. Terceiro' },
  { value: 'CONCLUIDA', label: 'Concluída' },
  { value: 'ENCERRADA', label: 'Encerrada' },
  { value: 'CANCELADA', label: 'Cancelada' },
  { value: 'REPROVADA', label: 'Reprovada' },
]

onMounted(async () => {
  carregando.value = true
  try {
    const resposta = await api.get('/ordem-servico/')
    ordens.value = resposta.data
  } catch (e) {
    console.error('Erro ao carregar ordens:', e)
  } finally {
    carregando.value = false
  }
})

const ordensFiltradas = computed(() => {
  return ordens.value.filter(o => {
    const statusOk = !filtroStatus.value || o.status_ordem_servico === filtroStatus.value
    const prioridadeOk = !filtroPrioridade.value || o.prioridade_urgencia === filtroPrioridade.value
    const buscaOk = !busca.value ||
      o.descricao_servico?.toLowerCase().includes(busca.value.toLowerCase()) ||
      (o.localizacao_nome || '').toLowerCase().includes(busca.value.toLowerCase())
    return statusOk && prioridadeOk && buscaOk
  })
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
    ABERTA: 'bg-blue-50 text-blue-700',
    APROVADA: 'bg-green-50 text-green-700',
    EM_EXECUCAO: 'bg-yellow-50 text-yellow-700',
    AGUARDANDO_MATERIAL: 'bg-orange-50 text-orange-700',
    AGUARDANDO_TERCEIRO: 'bg-purple-50 text-purple-700',
    CONCLUIDA: 'bg-teal-50 text-teal-700',
    ENCERRADA: 'bg-gray-100 text-gray-600',
    CANCELADA: 'bg-red-50 text-red-600',
    REPROVADA: 'bg-red-100 text-red-700',
  }
  return cores[status] || 'bg-gray-100 text-gray-500'
}

function labelStatus(status: string) {
  const labels: Record<string, string> = {
    ABERTA: 'Aberta', APROVADA: 'Aprovada', EM_EXECUCAO: 'Em Execução',
    AGUARDANDO_MATERIAL: 'Ag. Material', AGUARDANDO_TERCEIRO: 'Ag. Terceiro',
    CONCLUIDA: 'Concluída', ENCERRADA: 'Encerrada',
    CANCELADA: 'Cancelada', REPROVADA: 'Reprovada',
  }
  return labels[status] || status
}
</script>