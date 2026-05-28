<template>
  <div class="p-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-800">Ordens de Serviço</h1>
      <p class="text-sm text-gray-500 mt-1">Visão Geral do Sistema</p>
    </div>

    <div class="bg-white rounded-xl border border-gray-100 p-4 shadow-sm flex flex-wrap items-center justify-between gap-4 mb-6">
      <div class="flex items-center flex-wrap gap-4">
        <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Filtrar por</span>
        <select v-model="tipoAbaAtiva" class="bg-gray-50/80 border border-gray-200 text-gray-700 text-xs font-semibold rounded-lg px-3 py-2.5 outline-none focus:ring-2 focus:ring-blue-500 transition-all cursor-pointer">
          <option value="TODAS">Todos os tipos</option>
          <option value="CORRETIVA">Corretivas</option>
          <option value="PREVENTIVA">Preventivas</option>
        </select>
        <select v-model="filtroAtual" class="bg-gray-50/80 border border-gray-200 text-gray-700 text-xs font-semibold rounded-lg px-3 py-2.5 outline-none focus:ring-2 focus:ring-blue-500 transition-all cursor-pointer">
          <option value="TODAS">Todos os status</option>
          <option value="ABERTA">Abertas</option>
          <option value="EM_EXECUCAO">Em Execução</option>
          <option value="CONCLUIDA">Concluídas</option>
          <option value="CANCELADA">Canceladas</option>
        </select>
      </div>
      <div class="relative w-full md:w-80">
        <span class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-gray-400 text-sm">🔍</span>
        <input v-model="termoBusca" type="text" placeholder="Buscar por descrição ou local..." class="w-full bg-gray-50/80 border border-gray-200 text-gray-700 placeholder-gray-400 text-xs font-medium rounded-lg pl-9 pr-3 py-2.5 outline-none focus:ring-2 focus:ring-blue-500 transition-all" />
      </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-gray-50 border-b border-gray-100 text-xs text-gray-500 uppercase tracking-wider">
            <th class="p-4 font-semibold">Ordem / Tipo</th>
            <th class="p-4 font-semibold">Local / Prédio</th>
            <th class="p-4 font-semibold text-center">Status</th>
            <th class="p-4 font-semibold text-center">Abertura</th>
            <th class="p-4 font-semibold text-center">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading" class="border-b border-gray-50"><td colspan="5" class="p-8 text-center text-gray-400">Carregando ordens...</td></tr>
          <tr v-else-if="ordensFiltradas.length === 0" class="border-b border-gray-50"><td colspan="5" class="p-8 text-center text-gray-400">Nenhuma ordem encontrada.</td></tr>
          <tr v-else v-for="os in ordensFiltradas" :key="os.id_ordem_servico" class="border-b border-gray-50 hover:bg-gray-50 transition-colors">
            <td class="p-4">
              <div class="text-sm font-bold text-gray-800 mb-1">#{{ os.id_ordem_servico }}</div>
              <span v-if="os.tipo_manutencao === 'PREVENTIVA'" class="px-2 py-0.5 bg-purple-100 text-purple-700 rounded text-[10px] uppercase font-bold tracking-wider">Preventiva</span>
              <span v-else class="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-[10px] uppercase font-bold tracking-wider">Corretiva</span>
            </td>
            <td class="p-4 text-sm text-gray-600 truncate max-w-[200px]">{{ os.predio_nome || 'N/I' }} - {{ os.localizacao_nome || 'N/I' }}</td>
            <td class="p-4 text-center"><span :class="getStatusClass(os.status_ordem_servico)" class="px-3 py-1 rounded-full text-xs font-bold whitespace-nowrap">{{ formatarStatus(os.status_ordem_servico) }}</span></td>
            <td class="p-4 text-center text-sm text-gray-500">{{ formatarData(os.dt_abertura) }}</td>
            <td class="p-4 text-center"><button @click="abrirModalDetalhes(os)" class="text-blue-600 hover:text-blue-800 font-semibold text-sm">Ver Detalhes</button></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="modalAberto" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4 animate-fade-in">
      <div class="bg-white rounded-2xl w-full max-w-2xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
        <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
          <div><p class="text-xs font-bold text-gray-400 uppercase tracking-wider">Ordem de Serviço</p><h2 class="text-2xl font-bold text-gray-800 mt-1">#{{ osSelecionada?.id_ordem_servico }}</h2></div>
          <button @click="fecharModal" class="text-gray-400 hover:text-gray-700 p-2 rounded-full hover:bg-gray-200"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg></button>
        </div>
        <div class="p-6 overflow-y-auto">
          <div class="flex gap-3 mb-6">
            <span :class="getStatusClass(osSelecionada?.status_ordem_servico)" class="px-3 py-1 rounded-full text-sm font-bold">{{ formatarStatus(osSelecionada?.status_ordem_servico) }}</span>
          </div>
          <div class="grid grid-cols-2 gap-6 mb-6">
            <div class="bg-gray-50 p-4 rounded-xl"><p class="text-xs font-semibold text-gray-500 mb-1">LOCAL</p><p class="text-sm font-bold text-gray-800">{{ osSelecionada?.predio_nome }} - {{ osSelecionada?.localizacao_nome }}</p></div>
            <div class="bg-gray-50 p-4 rounded-xl"><p class="text-xs font-semibold text-gray-500 mb-1">SOLICITANTE</p><p class="text-sm font-bold text-gray-800">{{ osSelecionada?.tipo_manutencao === 'PREVENTIVA' ? 'Sistema' : osSelecionada?.solicitante_nome }}</p></div>
          </div>
          <div><p class="text-xs font-semibold text-gray-500 mb-2">DESCRIÇÃO</p><div class="p-4 bg-gray-50 rounded-xl border border-gray-100 text-sm text-gray-700 whitespace-pre-wrap">{{ osSelecionada?.descricao_servico }}</div></div>
        </div>
        <div class="p-6 border-t border-gray-100 flex justify-end gap-3 bg-gray-50">
          <button @click="fecharModal" class="px-6 py-2.5 rounded-lg font-bold text-gray-600 hover:bg-gray-200">Fechar</button>
          <button v-if="osSelecionada?.status_ordem_servico === 'ABERTA'" @click="cancelarOS" class="px-6 py-2.5 rounded-lg font-bold text-red-600 border border-red-200 hover:bg-red-50">Cancelar Ordem</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import Swal from 'sweetalert2'

const ordens = ref<any[]>([])
const loading = ref(true)
const tipoAbaAtiva = ref('TODAS')
const filtroAtual = ref('TODAS')
const termoBusca = ref('')
const modalAberto = ref(false)
const osSelecionada = ref<any>(null)

const ordensFiltradas = computed(() => {
  let resultado = ordens.value
  if (tipoAbaAtiva.value !== 'TODAS') resultado = resultado.filter(os => os.tipo_manutencao === tipoAbaAtiva.value)
  if (filtroAtual.value !== 'TODAS') resultado = resultado.filter(os => os.status_ordem_servico === filtroAtual.value)
  if (termoBusca.value.trim() !== '') {
    const termo = termoBusca.value.toLowerCase()
    resultado = resultado.filter(os => os.descricao_servico?.toLowerCase().includes(termo) || os.localizacao_nome?.toLowerCase().includes(termo))
  }
  return resultado
})

const formatarData = (dataIso: string) => dataIso ? new Date(dataIso).toLocaleDateString('pt-BR') : 'N/I'
const formatarStatus = (status: string) => {
  const mapa: Record<string, string> = { 'ABERTA': 'Aberta', 'EM_EXECUCAO': 'Em Execução', 'CONCLUIDA': 'Concluída', 'CANCELADA': 'Cancelada' }
  return mapa[status] || status
}
const getStatusClass = (status: string) => {
  const mapa: Record<string, string> = { 'ABERTA': 'bg-blue-100 text-blue-700', 'EM_EXECUCAO': 'bg-yellow-100 text-yellow-700', 'CONCLUIDA': 'bg-teal-100 text-teal-700', 'CANCELADA': 'bg-red-100 text-red-700' }
  return mapa[status] || 'bg-gray-100 text-gray-700'
}

async function carregarOrdens() {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    const response = await api.get('/ordem-servico/', { headers: { Authorization: `Bearer ${token}` } })
    ordens.value = response.data.dados || response.data
  } catch (error) { console.error(error) } finally { loading.value = false }
}

function abrirModalDetalhes(os: any) { osSelecionada.value = os; modalAberto.value = true }
function fecharModal() { modalAberto.value = false; osSelecionada.value = null }

async function cancelarOS() {
  const result = await Swal.fire({ title: 'Cancelar Ordem?', icon: 'warning', showCancelButton: true, confirmButtonColor: '#ef4444', confirmButtonText: 'Cancelar' })
  if (!result.isConfirmed) return
  try {
    await api.delete(`/ordem-servico/${osSelecionada.value.id_ordem_servico}/`, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
    Swal.fire('Cancelada!', '', 'success'); fecharModal(); carregarOrdens()
  } catch (error) { Swal.fire('Erro', '', 'error') }
}

onMounted(() => carregarOrdens())
</script>

<style scoped> .animate-fade-in { animation: fadeIn 0.2s ease-out; } @keyframes fadeIn { from { opacity: 0; transform: scale(0.98); } to { opacity: 1; transform: scale(1); } } </style>