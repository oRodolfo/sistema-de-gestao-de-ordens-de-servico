<template>
  <div class="p-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-800">Ordens de Serviço</h1>
      <p class="text-sm text-gray-500 mt-1">Gerencie, aprove e atribua técnicos às ordens sob sua responsabilidade</p>
    </div>

    <div class="flex gap-3 overflow-x-auto pb-4 mb-4">
      <button v-for="filtro in filtros" :key="filtro.valor" @click="filtroAtual = filtro.valor"
        :class="['px-5 py-2.5 rounded-full text-sm font-semibold transition-all whitespace-nowrap',
          filtroAtual === filtro.valor 
            ? 'bg-blue-700 text-white shadow-md' 
            : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50 hover:border-gray-300'
        ]">
        {{ filtro.label }}
        <span :class="['ml-1.5 px-2 py-0.5 rounded-full text-xs', 
          filtroAtual === filtro.valor ? 'bg-blue-800 text-white' : 'bg-gray-100 text-gray-500']">
          {{ contarPorStatus(filtro.valor) }}
        </span>
      </button>
    </div>

    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-gray-50 border-b border-gray-100 text-xs text-gray-500 uppercase tracking-wider">
            <th class="p-4 font-semibold">#</th>
            <th class="p-4 font-semibold">Local / Prédio</th>
            <th class="p-4 font-semibold">Descrição</th>
            <th class="p-4 font-semibold text-center">Status</th>
            <th class="p-4 font-semibold text-center">Prioridade</th>
            <th class="p-4 font-semibold text-center">Abertura</th>
            <th class="p-4 font-semibold text-center">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading" class="border-b border-gray-50">
            <td colspan="7" class="p-8 text-center text-gray-400">Carregando ordens...</td>
          </tr>
          <tr v-else-if="ordensFiltradas.length === 0" class="border-b border-gray-50">
            <td colspan="7" class="p-8 text-center text-gray-400">Nenhuma ordem encontrada para este filtro.</td>
          </tr>
          <tr v-else v-for="os in ordensFiltradas" :key="os.id_ordem_servico" class="border-b border-gray-50 hover:bg-gray-50 transition-colors">
            <td class="p-4 text-sm font-bold text-gray-700">#{{ os.id_ordem_servico }}</td>
            <td class="p-4 text-sm text-gray-600 truncate max-w-[200px]">{{ os.predio_nome || 'N/I' }} - {{ os.localizacao_nome || 'N/I' }}</td>
            <td class="p-4 text-sm text-gray-600 truncate max-w-[250px]">{{ os.descricao_servico }}</td>
            <td class="p-4 text-center">
              <span :class="getStatusClass(os.status_ordem_servico)" class="px-3 py-1 rounded-full text-xs font-bold whitespace-nowrap">
                {{ formatarStatus(os.status_ordem_servico) }}
              </span>
            </td>
            <td class="p-4 text-center">
              <span :class="os.prioridade_urgencia === 'ALTA' ? 'text-red-600 bg-red-100' : 'text-gray-600 bg-gray-100'" 
                    class="px-3 py-1 rounded-full text-xs font-bold">
                {{ os.prioridade_urgencia === 'ALTA' ? 'Urgente' : 'Normal' }}
              </span>
            </td>
            <td class="p-4 text-center text-sm text-gray-500">{{ formatarData(os.dt_abertura) }}</td>
            <td class="p-4 text-center">
              <button @click="abrirModalDetalhes(os)" class="text-blue-600 hover:text-blue-800 font-semibold text-sm transition-colors">Ver Detalhes</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="modalAberto" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4 animate-fade-in">
      <div class="bg-white rounded-2xl w-full max-w-2xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
        <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
          <div>
            <p class="text-xs font-bold text-gray-400 uppercase tracking-wider">Ordem de Serviço</p>
            <h2 class="text-2xl font-bold text-gray-800 mt-1">#{{ osSelecionada?.id_ordem_servico }}</h2>
          </div>
          <button @click="fecharModal" class="text-gray-400 hover:text-gray-700 p-2 rounded-full hover:bg-gray-200 transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        <div class="p-6 overflow-y-auto">
          <div class="flex gap-3 mb-6">
            <span :class="getStatusClass(osSelecionada?.status_ordem_servico)" class="px-3 py-1 rounded-full text-sm font-bold">
              {{ formatarStatus(osSelecionada?.status_ordem_servico) }}
            </span>
            <span :class="osSelecionada?.prioridade_urgencia === 'ALTA' ? 'text-red-600 bg-red-100' : 'text-gray-600 bg-gray-100'" class="px-3 py-1 rounded-full text-sm font-bold">
              {{ osSelecionada?.prioridade_urgencia === 'ALTA' ? 'Prioridade: Urgente' : 'Prioridade: Normal' }}
            </span>
          </div>

          <div class="grid grid-cols-2 gap-6 mb-6">
            <div class="bg-gray-50 p-4 rounded-xl">
              <p class="text-xs font-semibold text-gray-500 mb-1">LOCAL</p>
              <p class="text-sm font-bold text-gray-800">{{ osSelecionada?.predio_nome || 'N/I' }} - {{ osSelecionada?.localizacao_nome || 'N/I' }}</p>
            </div>
            <div class="bg-gray-50 p-4 rounded-xl">
              <p class="text-xs font-semibold text-gray-500 mb-1">DATA DE ABERTURA</p>
              <p class="text-sm font-bold text-gray-800">{{ formatarData(osSelecionada?.dt_abertura, true) }}</p>
            </div>
            <div class="bg-gray-50 p-4 rounded-xl">
              <p class="text-xs font-semibold text-gray-500 mb-1">SOLICITANTE</p>
              <p class="text-sm font-bold text-gray-800">{{ osSelecionada?.solicitante_nome || 'Usuário Anônimo' }}</p>
            </div>
            <div class="bg-gray-50 p-4 rounded-xl border border-blue-100 bg-blue-50/30">
              <p class="text-xs font-semibold text-blue-600 mb-1">TÉCNICO ATRIBUÍDO</p>
              <p class="text-sm font-bold text-gray-800">{{ osSelecionada?.tecnico_nome || 'Nenhum' }}</p>
            </div>
          </div>

          <div>
            <p class="text-xs font-semibold text-gray-500 mb-2">DESCRIÇÃO DO PROBLEMA</p>
            <div class="p-4 bg-gray-50 rounded-xl border border-gray-100 text-sm text-gray-700 whitespace-pre-wrap">
              {{ osSelecionada?.descricao_servico }}
            </div>
          </div>

          <div v-if="mostrandoAtribuicao" class="mt-6 p-4 border border-blue-200 bg-blue-50 rounded-xl">
            <p class="text-sm font-bold text-blue-800 mb-3">Selecione o Técnico para esta Ordem</p>
            <select v-model="tecnicoSelecionado" class="w-full p-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none">
              <option value="" disabled>Escolha um técnico...</option>
              <option v-for="tec in tecnicosDisponiveis" :key="tec.id_usuario" :value="tec.id_usuario">
                {{ tec.nome }} ({{ tec.email }})
              </option>
            </select>
            <div class="flex justify-end gap-3 mt-4">
              <button @click="mostrandoAtribuicao = false" class="px-4 py-2 text-sm text-gray-600 hover:bg-gray-200 rounded-lg font-semibold">Cancelar</button>
              <button @click="confirmarAtribuicao" :disabled="!tecnicoSelecionado" class="px-4 py-2 text-sm text-white bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 rounded-lg font-semibold shadow-md">Confirmar Atribuição</button>
            </div>
          </div>
        </div>

        <div class="p-6 border-t border-gray-100 flex justify-end gap-3 bg-gray-50" v-if="!mostrandoAtribuicao">
          <button @click="fecharModal" class="px-6 py-2.5 rounded-lg font-bold text-gray-600 hover:bg-gray-200 transition-colors">Fechar</button>
          
          <template v-if="osSelecionada?.status_ordem_servico === 'ABERTA'">
            <button @click="reprovarOS" class="px-6 py-2.5 rounded-lg font-bold text-red-600 border border-red-200 hover:bg-red-50 transition-colors">Reprovar</button>
            <button @click="iniciarAtribuicao" class="px-6 py-2.5 rounded-lg font-bold text-white bg-green-600 hover:bg-green-700 shadow-md transition-colors">Aprovar e Atribuir</button>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'

// Estados Reativos
const ordens = ref<any[]>([])
const loading = ref(true)
const filtroAtual = ref('TODAS')
const modalAberto = ref(false)
const osSelecionada = ref<any>(null)

// Estados para atribuição
const mostrandoAtribuicao = ref(false)
const tecnicosDisponiveis = ref<any[]>([])
const tecnicoSelecionado = ref<string>('')

// Filtros disponíveis
const filtros = [
  { label: 'Todas', valor: 'TODAS' },
  { label: 'Abertas', valor: 'ABERTA' },
  { label: 'Aprovadas', valor: 'APROVADA' },
  { label: 'Em Execução', valor: 'EM_EXECUCAO' },
  { label: 'Aguard. Material', valor: 'AGUARDANDO_MATERIAL' },
  { label: 'Concluídas', valor: 'CONCLUIDA' },
]

// Computed para filtrar a tabela
const ordensFiltradas = computed(() => {
  if (filtroAtual.value === 'TODAS') return ordens.value
  return ordens.value.filter(os => os.status_ordem_servico === filtroAtual.value)
})

// Funções Utilitárias
const contarPorStatus = (status: string) => {
  if (status === 'TODAS') return ordens.value.length
  return ordens.value.filter(os => os.status_ordem_servico === status).length
}

const formatarData = (dataIso: string, comHora = false) => {
  if (!dataIso) return 'N/I'
  const data = new Date(dataIso)
  if (comHora) return data.toLocaleString('pt-BR')
  return data.toLocaleDateString('pt-BR')
}

const formatarStatus = (status: string) => {
  const mapa: any = {
    'ABERTA': 'Aberta',
    'APROVADA': 'Aprovada',
    'EM_EXECUCAO': 'Em Execução',
    'AGUARDANDO_MATERIAL': 'Aguard. Material',
    'AGUARDANDO_TERCEIRO': 'Aguard. Terceiro',
    'CONCLUIDA': 'Concluída',
    'REPROVADA': 'Reprovada',
    'CANCELADA': 'Cancelada',
    'ENCERRADA': 'Encerrada'
  }
  return mapa[status] || status
}

const getStatusClass = (status: string) => {
  const mapa: any = {
    'ABERTA': 'bg-blue-100 text-blue-700',
    'APROVADA': 'bg-emerald-100 text-emerald-700',
    'EM_EXECUCAO': 'bg-yellow-100 text-yellow-700',
    'AGUARDANDO_MATERIAL': 'bg-orange-100 text-orange-700',
    'CONCLUIDA': 'bg-teal-100 text-teal-700',
    'REPROVADA': 'bg-red-100 text-red-700',
    'CANCELADA': 'bg-red-100 text-red-700',
  }
  return mapa[status] || 'bg-gray-100 text-gray-700'
}

// Ações da API
async function carregarOrdens() {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    const response = await api.get('/ordem-servico/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    ordens.value = response.data.dados || response.data
  } catch (error) {
    console.error("Erro ao carregar ordens:", error)
  } finally {
    loading.value = false
  }
}

async function carregarTecnicos() {
  try {
    const token = localStorage.getItem('token')
    const response = await api.get('/usuario/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    const usuarios = response.data.dados || response.data
    // Filtra para pegar apenas quem tem o cargo TECNICO
    tecnicosDisponiveis.value = usuarios.filter((u: any) => u.cargo === 'TECNICO')
  } catch (error) {
    console.error("Erro ao carregar técnicos:", error)
  }
}

// Controles do Modal
function abrirModalDetalhes(os: any) {
  osSelecionada.value = os
  mostrandoAtribuicao.value = false
  tecnicoSelecionado.value = ''
  modalAberto.value = true
}

function fecharModal() {
  modalAberto.value = false
  osSelecionada.value = null
}

function iniciarAtribuicao() {
  if (tecnicosDisponiveis.value.length === 0) {
    carregarTecnicos()
  }
  mostrandoAtribuicao.value = true
}

// Ações de Gestão (Requisições PATCH)
async function reprovarOS() {
  if (!confirm("Tem certeza que deseja reprovar esta Ordem de Serviço?")) return

  try {
    const token = localStorage.getItem('token')
    await api.patch(`/ordem-servico/${osSelecionada.value.id_ordem_servico}/`, 
      { status_ordem_servico: 'REPROVADA' },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    alert("Ordem de Serviço reprovada com sucesso!")
    fecharModal()
    carregarOrdens() // Recarrega a tabela
  } catch (error) {
    console.error("Erro ao reprovar OS:", error)
    alert("Erro ao reprovar a ordem.")
  }
}

async function confirmarAtribuicao() {
  try {
    const token = localStorage.getItem('token')
    await api.patch(`/ordem-servico/${osSelecionada.value.id_ordem_servico}/atribuir-tecnico/`, 
      { tecnico: tecnicoSelecionado.value },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    alert("Técnico atribuído com sucesso! A Ordem agora está Aprovada.")
    fecharModal()
    carregarOrdens() // Recarrega a tabela
  } catch (error) {
    console.error("Erro ao atribuir técnico:", error)
    alert("Erro ao atribuir técnico. Verifique as permissões.")
  }
}

onMounted(() => {
  carregarOrdens()
})
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.2s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.98); }
  to { opacity: 1; transform: scale(1); }
}
</style>