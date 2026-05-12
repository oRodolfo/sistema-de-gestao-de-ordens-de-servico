<template>
  <div class="p-8">

    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Ordens de Serviço</h1>
      <p class="text-sm text-gray-500 mt-1">Gerencie e aprove as ordens sob sua responsabilidade</p>
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
              <button v-if="ordem.status_ordem_servico === 'ABERTA'" @click="abrirAtribuir(ordem)"
                class="text-green-600 hover:text-green-800 font-semibold cursor-pointer">Aprovar</button>
              <button v-if="ordem.status_ordem_servico === 'ABERTA'" @click="reprovarOrdem(ordem)"
                class="text-red-500 hover:text-red-700 font-semibold cursor-pointer">Reprovar</button>
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
          <div>
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Técnico</p>
            <p class="text-sm text-gray-800">{{ ordemSelecionada.tecnico || 'Não atribuído' }}</p>
          </div>
        </div>
        <div class="mb-6">
          <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Descrição</p>
          <p class="text-sm text-gray-700 bg-gray-50 rounded-lg p-4 leading-relaxed">{{ ordemSelecionada.descricao_servico }}</p>
        </div>
        <div class="flex justify-end gap-3">
          <button v-if="ordemSelecionada.status_ordem_servico === 'ABERTA'" @click="reprovarOrdem(ordemSelecionada); mostrarModalDetalhe = false"
            class="px-5 py-2 rounded-lg bg-red-500 text-white font-semibold hover:bg-red-600 cursor-pointer">Reprovar</button>
          <button v-if="ordemSelecionada.status_ordem_servico === 'ABERTA'" @click="mostrarModalDetalhe = false; abrirAtribuir(ordemSelecionada)"
            class="px-5 py-2 rounded-lg bg-green-600 text-white font-semibold hover:bg-green-700 cursor-pointer">Aprovar e Atribuir</button>
          <button @click="mostrarModalDetalhe = false"
            class="px-5 py-2 rounded-lg bg-blue-800 text-white font-semibold hover:bg-blue-600 cursor-pointer">Fechar</button>
        </div>
      </div>
    </div>

    <!-- Modal Atribuir Técnico -->
    <div v-if="mostrarModalAtribuir && ordemSelecionada" @click.self="mostrarModalAtribuir = false"
      class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
      <div class="bg-white rounded-xl p-8 w-full max-w-md shadow-xl">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-bold text-gray-800">Atribuir Técnico</h2>
          <button @click="mostrarModalAtribuir = false" class="text-gray-400 hover:text-gray-600 cursor-pointer text-xl">✕</button>
        </div>
        <p class="text-sm text-gray-500 mb-4">
          Selecione um técnico para a ordem <span class="font-semibold text-gray-800">#{{ ordemSelecionada.id_ordem_servico }}</span>
        </p>
        <div class="flex flex-col gap-2 mb-6">
          <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Técnico</label>
          <select v-model="tecnicoSelecionado"
            class="border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-blue-600 cursor-pointer">
            <option value="">Selecione um técnico</option>
            <option v-for="tec in tecnicos" :key="tec.id" :value="tec.id">{{ tec.nome }}</option>
          </select>
        </div>
        <div class="flex gap-3">
          <button @click="mostrarModalAtribuir = false"
            class="flex-1 py-3 rounded-lg border border-gray-300 text-gray-600 font-semibold hover:bg-gray-50 cursor-pointer">Cancelar</button>
          <button @click="confirmarAtribuicao"
            class="flex-1 py-3 rounded-lg bg-blue-800 text-white font-semibold hover:bg-blue-600 cursor-pointer">Confirmar</button>
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
const mostrarModalAtribuir = ref(false)
const tecnicoSelecionado = ref('')

const statusOpcoes = [
  { value: '', label: 'Todas' },
  { value: 'ABERTA', label: 'Abertas' },
  { value: 'APROVADA', label: 'Aprovadas' },
  { value: 'EM_EXECUCAO', label: 'Em Execução' },
  { value: 'AGUARDANDO_MATERIAL', label: 'Aguard. Material' },
  { value: 'CONCLUIDA', label: 'Concluídas' },
  { value: 'REPROVADA', label: 'Reprovadas' },
]

const tecnicos = [
  { id: 1, nome: 'Carlos Técnico' },
  { id: 2, nome: 'Roberto Técnico' },
  { id: 3, nome: 'Ana Técnica' },
  { id: 4, nome: 'Paulo Técnico' },
]

const ordens = ref([
  { id_ordem_servico: 1, localizacao: 'Bloco A - Sala 101', status_ordem_servico: 'ABERTA', prioridade_urgencia: 'SIM', dt_abertura: '2026-04-28T10:30:00', descricao_servico: 'Ar condicionado com defeito, não resfria o ambiente.', solicitante: 'João Silva', tecnico: null },
  { id_ordem_servico: 2, localizacao: 'Biblioteca - Térreo', status_ordem_servico: 'EM_EXECUCAO', prioridade_urgencia: 'NAO', dt_abertura: '2026-04-27T08:15:00', descricao_servico: 'Troca de lâmpadas queimadas no corredor principal.', solicitante: 'Maria Souza', tecnico: 'Carlos Técnico' },
  { id_ordem_servico: 3, localizacao: 'Laboratório 3 - Bloco B', status_ordem_servico: 'AGUARDANDO_MATERIAL', prioridade_urgencia: 'SIM', dt_abertura: '2026-04-25T14:00:00', descricao_servico: 'Tomadas sem energia, necessário trocar disjuntor.', solicitante: 'Pedro Costa', tecnico: 'Carlos Técnico' },
  { id_ordem_servico: 4, localizacao: 'Secretaria - Bloco C', status_ordem_servico: 'CONCLUIDA', prioridade_urgencia: 'NAO', dt_abertura: '2026-04-20T09:00:00', descricao_servico: 'Reparo na fechadura da porta principal.', solicitante: 'Ana Lima', tecnico: 'Roberto Técnico' },
  { id_ordem_servico: 5, localizacao: 'Cantina - Térreo', status_ordem_servico: 'ABERTA', prioridade_urgencia: 'NAO', dt_abertura: '2026-04-29T11:45:00', descricao_servico: 'Vazamento de água na pia da cozinha.', solicitante: 'Lucas Mendes', tecnico: null },
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

function abrirAtribuir(ordem: any) {
  ordemSelecionada.value = ordem
  tecnicoSelecionado.value = ''
  mostrarModalAtribuir.value = true
}

function reprovarOrdem(ordem: any) {
  ordem.status_ordem_servico = 'REPROVADA'
}

function confirmarAtribuicao() {
  if (!tecnicoSelecionado.value) return
  const tec = tecnicos.find(t => t.id === Number(tecnicoSelecionado.value))
  if (tec && ordemSelecionada.value) {
    ordemSelecionada.value.tecnico = tec.nome
    ordemSelecionada.value.status_ordem_servico = 'APROVADA'
  }
  mostrarModalAtribuir.value = false
  tecnicoSelecionado.value = ''
}

function corStatus(status: string) {
  const cores: Record<string, string> = {
    ABERTA: 'bg-blue-100 text-blue-700',
    APROVADA: 'bg-green-100 text-green-700',
    EM_EXECUCAO: 'bg-yellow-100 text-yellow-700',
    AGUARDANDO_MATERIAL: 'bg-orange-100 text-orange-700',
    CONCLUIDA: 'bg-teal-100 text-teal-700',
    REPROVADA: 'bg-red-100 text-red-700',
  }
  return cores[status] || 'bg-gray-100 text-gray-600'
}

function labelStatus(status: string) {
  const labels: Record<string, string> = {
    ABERTA: 'Aberta', APROVADA: 'Aprovada', EM_EXECUCAO: 'Em Execução',
    AGUARDANDO_MATERIAL: 'Aguard. Material', CONCLUIDA: 'Concluída', REPROVADA: 'Reprovada',
  }
  return labels[status] || status
}
</script>