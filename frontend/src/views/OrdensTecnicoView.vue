<template>
  <div class="p-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-800">Minhas Ordens de Serviço</h1>
      <p class="text-sm text-gray-500 mt-1">Gira a execução dos serviços que lhe foram atribuídos</p>
    </div>

    <!-- Barra de Filtros Premium -->
    <div class="bg-white rounded-xl border border-gray-100 p-4 shadow-sm flex flex-wrap items-center justify-between gap-4 mb-6">
      <div class="flex items-center flex-wrap gap-3">
        <span class="text-xs font-bold text-gray-400 uppercase tracking-wider mr-1">Filtrar por</span>
        
        <select v-model="tipoAbaAtiva" class="bg-gray-50/80 border border-gray-200 text-gray-700 text-xs font-semibold rounded-lg px-3 py-2.5 outline-none focus:ring-2 focus:ring-blue-500 transition-all cursor-pointer">
          <option value="TODAS">Todos os tipos</option>
          <option value="CORRETIVA">Corretivas</option>
          <option value="PREVENTIVA">Preventivas</option>
        </select>
        
        <select v-model="filtroAtual" class="bg-gray-50/80 border border-gray-200 text-gray-700 text-xs font-semibold rounded-lg px-3 py-2.5 outline-none focus:ring-2 focus:ring-blue-500 transition-all cursor-pointer">
          <option value="TODAS">Todos os status</option>
          <option value="APROVADA">Para Iniciar (Aprovadas)</option>
          <option value="EM_EXECUCAO">Em Execução</option>
          <option value="AGUARDANDO_MATERIAL">Falta Material / Pausadas</option>
          <option value="CONCLUIDA">Concluídas</option>
        </select>

        <select v-model="filtroPrioridade" class="bg-gray-50/80 border border-gray-200 text-gray-700 text-xs font-semibold rounded-lg px-3 py-2.5 outline-none focus:ring-2 focus:ring-blue-500 transition-all cursor-pointer">
          <option value="TODAS">Todas as prioridades</option>
          <option value="SIM">Urgente</option>
          <option value="NAO">Normal</option>
        </select>

        <!-- Filtro de Prédio -->
        <select v-model="filtroPredio" class="bg-gray-50/80 border border-gray-200 text-gray-700 text-xs font-semibold rounded-lg px-3 py-2.5 outline-none focus:ring-2 focus:ring-blue-500 transition-all cursor-pointer max-w-[200px] truncate">
          <option value="TODOS">Todos os Prédios</option>
          <option v-for="predio in prediosUnicos" :key="predio" :value="predio">{{ predio }}</option>
        </select>
      </div>
      
      <div class="relative w-full xl:w-72">
        <span class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-gray-400 text-sm">🔍</span>
        <input v-model="termoBusca" type="text" placeholder="Buscar por descrição ou local..." class="w-full bg-gray-50/80 border border-gray-200 text-gray-700 placeholder-gray-400 text-xs font-medium rounded-lg pl-9 pr-3 py-2.5 outline-none focus:ring-2 focus:ring-blue-500 transition-all cursor-text" />
      </div>
    </div>

    <!-- Tabela -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-gray-50 border-b border-gray-100 text-xs text-gray-500 uppercase tracking-wider">
            <th class="p-4 font-semibold">Ordem / Tipo</th>
            <th class="p-4 font-semibold">Local / Prédio</th>
            <th class="p-4 font-semibold">Descrição</th>
            <th class="p-4 font-semibold text-center">Status</th>
            <th class="p-4 font-semibold text-center">Prioridade</th>
            <th class="p-4 font-semibold text-center">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading" class="border-b border-gray-50"><td colspan="6" class="p-8 text-center text-gray-400 font-medium">A carregar ordens...</td></tr>
          <tr v-else-if="ordensFiltradas.length === 0" class="border-b border-gray-50"><td colspan="6" class="p-8 text-center text-gray-400 font-medium">Nenhuma ordem encontrada.</td></tr>
          <tr v-else v-for="os in ordensFiltradas" :key="os.id_ordem_servico" class="border-b border-gray-50 hover:bg-gray-50/80 transition-colors">
            <td class="p-4">
              <div class="text-sm font-bold text-gray-800 mb-1">#{{ os.id_ordem_servico }}</div>
              <span v-if="os.tipo_manutencao === 'PREVENTIVA'" class="px-2 py-0.5 bg-purple-100 text-purple-700 rounded text-[10px] uppercase font-bold tracking-wider">Preventiva</span>
              <span v-else class="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-[10px] uppercase font-bold tracking-wider">Corretiva</span>
            </td>
            <td class="p-4 text-sm text-gray-600 truncate max-w-[200px]">{{ os.predio_nome || 'N/I' }} - {{ os.localizacao_nome || 'N/I' }}</td>
            
            <td class="p-4 text-sm text-gray-600 truncate max-w-[250px]" :title="extrairProblema(os.descricao_servico)">
              {{ extrairProblema(os.descricao_servico) }}
            </td>

            <td class="p-4 text-center"><span :class="getStatusClass(os.status_ordem_servico)" class="px-3 py-1 rounded-full text-xs font-bold whitespace-nowrap">{{ formatarStatus(os.status_ordem_servico) }}</span></td>
            
            <td class="p-4 text-center">
              <span :class="os.prioridade_urgencia === 'SIM' ? 'text-red-600 bg-red-100' : 'text-gray-600 bg-gray-100'" class="px-3 py-1 rounded-full text-xs font-bold">
                {{ os.prioridade_urgencia === 'SIM' ? 'Urgente' : 'Normal' }}
              </span>
            </td>

            <td class="p-4 text-center"><button @click="abrirModalDetalhes(os)" class="text-blue-600 hover:text-white hover:bg-blue-600 font-bold border border-blue-200 px-3 py-1.5 rounded-lg transition-all shadow-sm cursor-pointer">Abrir Ordem</button></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Técnico -->
    <div v-if="modalAberto" @click.self="fecharModal" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4 animate-fade-in">
      <div class="bg-white rounded-2xl w-full max-w-2xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
        <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
          <div>
            <p class="text-xs font-bold text-gray-400 uppercase tracking-wider">Execução do Serviço</p>
            <h2 class="text-2xl font-bold text-gray-800 mt-1">#{{ osSelecionada?.id_ordem_servico }}</h2>
          </div>
          <button @click="fecharModal" class="text-gray-400 hover:text-gray-700 p-2 rounded-full hover:bg-gray-200 transition-colors cursor-pointer">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto">
          <div class="flex items-center gap-3 mb-6">
            <span :class="getStatusClass(osSelecionada?.status_ordem_servico)" class="px-3 py-1.5 rounded-full text-sm font-bold">{{ formatarStatus(osSelecionada?.status_ordem_servico) }}</span>
            
            <!-- Etiqueta Interativa de Prioridade -->
            <div class="relative">
              <select 
                :value="osSelecionada?.prioridade_urgencia"
                @change="alterarPrioridade($event.target.value)"
                :class="[
                  'pl-3 pr-8 py-1.5 rounded-full text-sm font-bold outline-none cursor-pointer appearance-none border transition-colors',
                  osSelecionada?.prioridade_urgencia === 'SIM' ? 'text-red-700 bg-red-50 border-red-200 hover:bg-red-100' : 'text-gray-700 bg-gray-50 border-gray-200 hover:bg-gray-100'
                ]"
              >
                <option value="NAO">Prioridade: Normal</option>
                <option value="SIM">Prioridade: Urgente</option>
              </select>
              <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2" :class="osSelecionada?.prioridade_urgencia === 'SIM' ? 'text-red-500' : 'text-gray-500'">
                <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
              </div>
            </div>
          </div>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-6">
            <div class="bg-gray-50 p-4 rounded-xl"><p class="text-xs font-semibold text-gray-500 mb-1">LOCAL</p><p class="text-sm font-bold text-gray-800">{{ osSelecionada?.predio_nome || 'N/I' }} - {{ osSelecionada?.localizacao_nome || 'N/I' }}</p></div>
            <div class="bg-gray-50 p-4 rounded-xl"><p class="text-xs font-semibold text-gray-500 mb-1">SOLICITANTE</p><p class="text-sm font-bold text-gray-800">{{ extrairSolicitante(osSelecionada) }}</p></div>
          </div>
          
          <div>
            <p class="text-xs font-semibold text-gray-500 mb-2">DESCRIÇÃO DO PROBLEMA</p>
            <div class="p-4 bg-gray-50 rounded-xl border border-gray-100 text-sm text-gray-700 whitespace-pre-wrap">{{ extrairProblema(osSelecionada?.descricao_servico) }}</div>
          </div>
        </div>

        <!-- Rodapé do Modal com Ações de Execução (Responsivo) -->
        <div class="p-5 sm:p-6 border-t border-gray-100 flex flex-wrap justify-end gap-2 sm:gap-3 bg-gray-50">
          <button @click="fecharModal" class="px-4 sm:px-6 py-2.5 rounded-lg font-bold text-gray-600 hover:bg-gray-200 transition-colors cursor-pointer w-full sm:w-auto">
            Fechar
          </button>
          
          <template v-if="osSelecionada?.status_ordem_servico === 'APROVADA'">
            <button @click="alterarStatus('EM_EXECUCAO', 'Deseja iniciar a execução deste serviço agora?', 'Sim, Iniciar', '#2563eb')" class="px-4 sm:px-6 py-2.5 rounded-lg font-bold text-white bg-blue-600 hover:bg-blue-700 shadow-md transition-all cursor-pointer w-full sm:w-auto">
              ▶ Iniciar Execução
            </button>
          </template>

          <template v-if="osSelecionada?.status_ordem_servico === 'EM_EXECUCAO'">
            <button @click="alterarStatus('AGUARDANDO_MATERIAL', 'Falta algum material para terminar o serviço?', 'Pausar Serviço', '#ea580c')" class="px-4 sm:px-6 py-2.5 rounded-lg font-bold text-orange-600 border border-orange-200 hover:bg-orange-50 transition-colors cursor-pointer w-full sm:w-auto">
              ⏸ Falta Material
            </button>
            <button @click="alterarStatus('CONCLUIDA', 'Tem a certeza que o serviço foi finalizado?', 'Sim, Concluir', '#0d9488')" class="px-4 sm:px-6 py-2.5 rounded-lg font-bold text-white bg-teal-600 hover:bg-teal-700 shadow-md transition-all cursor-pointer w-full sm:w-auto">
              ✅ Concluir Serviço
            </button>
          </template>

          <template v-if="['AGUARDANDO_MATERIAL', 'AGUARDANDO_TERCEIRO'].includes(osSelecionada?.status_ordem_servico)">
            <button @click="alterarStatus('EM_EXECUCAO', 'Os materiais chegaram? Deseja retomar o serviço?', 'Sim, Retomar', '#2563eb')" class="px-4 sm:px-6 py-2.5 rounded-lg font-bold text-white bg-blue-600 hover:bg-blue-700 shadow-md transition-all cursor-pointer w-full sm:w-auto">
              ▶ Retomar Execução
            </button>
          </template>
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
const filtroPrioridade = ref('TODAS')
const filtroPredio = ref('TODOS')
const termoBusca = ref('')

const modalAberto = ref(false)
const osSelecionada = ref<any>(null)

// Computed inteligente para listar Prédios únicos
const prediosUnicos = computed(() => {
  const nomes = new Set(ordens.value.map(os => os.predio_nome).filter(Boolean))
  return Array.from(nomes).sort()
})

// Funções Inteligentes para limpar o texto gerado pelo Totem
const extrairSolicitante = (os: any) => {
  if (!os) return ''
  if (os.tipo_manutencao === 'PREVENTIVA') return 'Sistema (Automático)'
  const match = os.descricao_servico?.match(/\[(.*?)\]/);
  if (match) return match[1]; 
  return os.solicitante_nome || 'Usuário Anônimo / Totem';
}

const extrairProblema = (descricao: string) => {
  if (!descricao) return 'Sem descrição detalhada.'
  return descricao.replace(/\[.*?\]\s*(-\s*Local:.*?\s*)?-\s*(Problema:\s*)?/, '').trim();
}

const authHeader = () => {
  const token = localStorage.getItem('token')
  return { headers: { Authorization: `Bearer ${token}` } }
}

const ordensFiltradas = computed(() => {
  let resultado = ordens.value
  if (tipoAbaAtiva.value !== 'TODAS') resultado = resultado.filter(os => os.tipo_manutencao === tipoAbaAtiva.value)
  if (filtroAtual.value !== 'TODAS') resultado = resultado.filter(os => os.status_ordem_servico === filtroAtual.value)
  if (filtroPrioridade.value !== 'TODAS') resultado = resultado.filter(os => os.prioridade_urgencia === filtroPrioridade.value)
  if (filtroPredio.value !== 'TODOS') resultado = resultado.filter(os => os.predio_nome === filtroPredio.value)
  
  if (termoBusca.value.trim() !== '') {
    const termo = termoBusca.value.toLowerCase()
    resultado = resultado.filter(os => 
      os.descricao_servico?.toLowerCase().includes(termo) || 
      os.localizacao_nome?.toLowerCase().includes(termo) || 
      os.predio_nome?.toLowerCase().includes(termo)
    )
  }
  return resultado
})

const formatarStatus = (status: string) => {
  const mapa: Record<string, string> = { 'APROVADA': 'Para Iniciar', 'EM_EXECUCAO': 'Em Execução', 'AGUARDANDO_MATERIAL': 'Falta Material', 'AGUARDANDO_TERCEIRO': 'Aguard. Terceiro', 'CONCLUIDA': 'Concluída', 'ENCERRADA': 'Encerrada' }
  return mapa[status] || status
}

const getStatusClass = (status: string) => {
  const mapa: Record<string, string> = { 'APROVADA': 'bg-emerald-100 text-emerald-700 border border-emerald-200', 'EM_EXECUCAO': 'bg-yellow-100 text-yellow-700 border border-yellow-200', 'AGUARDANDO_MATERIAL': 'bg-orange-100 text-orange-700 border border-orange-200', 'CONCLUIDA': 'bg-teal-100 text-teal-700 border border-teal-200' }
  return mapa[status] || 'bg-gray-100 text-gray-700 border border-gray-200'
}

async function carregarOrdens() {
  loading.value = true
  try {
    const response = await api.get('/ordem-servico/', authHeader())
    ordens.value = response.data.dados || response.data
  } catch (error) { 
    console.error(error) 
  } finally { 
    loading.value = false 
  }
}

function abrirModalDetalhes(os: any) { 
  osSelecionada.value = os
  modalAberto.value = true 
}

function fecharModal() { 
  modalAberto.value = false
  osSelecionada.value = null 
}

async function alterarPrioridade(novaPrioridade: string) {
  try {
    await api.patch(`/ordem-servico/${osSelecionada.value.id_ordem_servico}/`, { prioridade_urgencia: novaPrioridade }, authHeader())
    osSelecionada.value.prioridade_urgencia = novaPrioridade
    
    const Toast = Swal.mixin({ toast: true, position: 'top-end', showConfirmButton: false, timer: 3000, timerProgressBar: true })
    Toast.fire({ icon: 'success', title: 'Prioridade alterada com sucesso!' })
    
    carregarOrdens()
  } catch (error) {
    Swal.fire({ title: 'Erro', text: 'Não foi possível alterar a prioridade.', icon: 'error' })
  }
}

async function alterarStatus(novoStatus: string, mensagem: string, textoBotao: string, corBotao: string) {
  const result = await Swal.fire({ 
    title: 'Atenção', text: mensagem, icon: 'question', showCancelButton: true, confirmButtonColor: corBotao, cancelButtonColor: '#6b7280', confirmButtonText: textoBotao, cancelButtonText: 'Cancelar', customClass: { confirmButton: 'cursor-pointer', cancelButton: 'cursor-pointer' }
  })
  
  if (!result.isConfirmed) return
  
  try {
    await api.patch(`/ordem-servico/${osSelecionada.value.id_ordem_servico}/`, { status_ordem_servico: novoStatus }, authHeader())
    
    let msgSucesso = 'Status atualizado com sucesso.'
    if (novoStatus === 'CONCLUIDA') msgSucesso = 'Fantástico! Ordem finalizada.'
    if (novoStatus === 'EM_EXECUCAO') msgSucesso = 'Bom trabalho! O relógio está a contar.'

    Swal.fire({ title: 'Feito!', text: msgSucesso, icon: 'success', customClass: { confirmButton: 'cursor-pointer' }})
    fecharModal()
    carregarOrdens()
  } catch (error) { 
    Swal.fire({ title: 'Erro', text: 'Falha ao atualizar o status da ordem.', icon: 'error', customClass: { confirmButton: 'cursor-pointer' }}) 
  }
}

onMounted(() => carregarOrdens())
</script>

<style scoped> 
.animate-fade-in { animation: fadeIn 0.2s ease-out; } 
@keyframes fadeIn { from { opacity: 0; transform: scale(0.98); } to { opacity: 1; transform: scale(1); } } 
</style>