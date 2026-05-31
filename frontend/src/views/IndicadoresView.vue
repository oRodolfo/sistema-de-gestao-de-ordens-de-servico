<template>
  <div class="p-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-800">Visão Global da Instituição</h1>
      <p class="text-sm text-gray-500 mt-1">Acompanhamento consolidado de performance técnica da FHO</p>
    </div>

    <div class="grid grid-cols-2 gap-4 mb-8 lg:grid-cols-4">
      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer relative overflow-hidden group">
        <div class="bg-blue-600 absolute -right-4 -top-4 w-24 h-24 rounded-full opacity-10 transition-transform group-hover:scale-110"></div>
        <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 flex items-center gap-2"><span>🏢</span> Volume Total FHO</p>
        <p class="text-4xl font-extrabold tracking-tight mb-1 text-blue-700">{{ dadosBrutos.totalOrdens }}</p>
        <p class="text-[11px] text-gray-400 font-semibold uppercase">Ordens Registradas</p>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer relative overflow-hidden group">
        <div class="bg-orange-600 absolute -right-4 -top-4 w-24 h-24 rounded-full opacity-10 transition-transform group-hover:scale-110"></div>
        <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 flex items-center gap-2"><span>⏳</span> Fila de Triagem</p>
        <p class="text-4xl font-extrabold tracking-tight mb-1 text-orange-600">{{ dadosBrutos.abertas }}</p>
        <p class="text-[11px] text-gray-400 font-semibold uppercase">Pendentes de Gestor</p>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer relative overflow-hidden group">
        <div class="bg-emerald-500 absolute -right-4 -top-4 w-24 h-24 rounded-full opacity-10 transition-transform group-hover:scale-110"></div>
        <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 flex items-center gap-2"><span>✅</span> Total Solucionado</p>
        <p class="text-4xl font-extrabold tracking-tight mb-1 text-emerald-600">{{ dadosBrutos.concluidas }}</p>
        <p class="text-[11px] text-gray-400 font-semibold uppercase">Histórico Finalizado</p>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer relative overflow-hidden group">
        <div class="bg-purple-600 absolute -right-4 -top-4 w-24 h-24 rounded-full opacity-10 transition-transform group-hover:scale-110"></div>
        <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 flex items-center gap-2"><span>⏱️</span> Tempo Médio </p>
        <p class="text-4xl font-extrabold tracking-tight mb-1 text-purple-700">{{ dadosBrutos.tempo_medio || '0d' }}</p>
        <p class="text-[11px] text-gray-400 font-semibold uppercase">Média de Resolução</p>
      </div>
    </div>

    <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">

      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 flex flex-col">
        <h2 class="text-sm font-bold text-gray-800 mb-6 uppercase tracking-wider">Status Geral de Manutenções</h2>
        <div class="space-y-4 flex-1">
          <div v-for="item in ordensPorStatus" :key="item.status" class="flex items-center gap-4 cursor-pointer group">
            <span class="w-36 text-xs font-semibold text-gray-500 group-hover:text-gray-800 transition-colors shrink-0">{{ item.label }}</span>
            <div class="flex-1 bg-gray-50 rounded-full h-2.5 border border-gray-100 overflow-hidden">
              <div class="h-2.5 rounded-full transition-all duration-1000 ease-out relative" 
                   :class="item.corGradiente"
                   :style="{ width: `${dadosBrutos.totalOrdens > 0 ? (item.quantidade / dadosBrutos.totalOrdens) * 100 : 0}%` }">
              </div>
            </div>
            <span class="text-xs font-bold w-8 text-right transition-colors" :class="item.corTexto">{{ item.quantidade || 0 }}</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 flex flex-col">
        <h2 class="text-sm font-bold text-gray-800 mb-6 uppercase tracking-wider flex items-center justify-between">
          <span>Ranking de Técnicos (FHO)</span>
          <span class="text-[10px] text-blue-600 bg-blue-50 px-2 py-1 rounded-full border border-blue-100">ALTA PERFORMANCE</span>
        </h2>
        <div class="space-y-4 overflow-y-auto max-h-[250px] pr-2 flex-1">
          <div v-if="!tecnicos.length" class="h-full flex flex-col items-center justify-center py-6">
            <span class="text-3xl mb-2 opacity-50">🏆</span>
            <p class="text-sm text-gray-400 font-medium">O ranking será gerado assim que as ordens forem atribuídas.</p>
          </div>
          
          <div v-else v-for="(tec, index) in tecnicos" :key="tec.nome" class="flex items-center gap-4 p-3 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer border border-transparent hover:border-gray-100">
            <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-100 to-blue-50 flex items-center justify-center font-bold text-blue-700 text-xs shadow-inner border border-blue-200">
              #{{ index + 1 }}
            </div>
            <div class="flex-1">
              <p class="text-sm font-bold text-gray-800">{{ tec.nome }}</p>
              <div class="flex items-center gap-2 mt-1">
                <div class="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                   <div class="h-full bg-emerald-500 rounded-full" :style="{ width: `${tec.total > 0 ? (tec.concluidas / tec.total) * 100 : 0}%` }"></div>
                </div>
                <p class="text-[10px] text-gray-500 font-bold whitespace-nowrap">{{ tec.concluidas }} / {{ tec.total }} concluídas</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 class="text-sm font-bold text-gray-800 mb-6 uppercase tracking-wider flex items-center gap-2">
          <span class="text-red-500">⚠️</span> Gargalos da Instituição
        </h2>
        <div class="space-y-2">
          <div v-for="item in pendentes" :key="item.label" class="flex items-center justify-between p-3 rounded-lg border border-gray-100 hover:bg-gray-50 transition-colors cursor-pointer">
            <span class="text-xs font-semibold text-gray-600">{{ item.label }}</span>
            <span class="text-sm font-extrabold px-3 py-1 rounded-md" :class="item.bgCor + ' ' + item.cor">{{ item.valor }}</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 flex flex-col">
        <h2 class="text-sm font-bold text-gray-800 mb-6 uppercase tracking-wider">Histórico de Resoluções (6 Semanas)</h2>
        <div class="flex items-end justify-between gap-2 h-40 flex-1 mt-auto pb-2 relative">
          
          <div v-if="maxSemana === 0" class="absolute inset-0 flex items-center justify-center">
             <p class="text-sm text-gray-400 font-medium italic">Aguardando as primeiras conclusões do mês.</p>
          </div>

          <div v-else v-for="semana in semanas" :key="semana.label" class="flex-1 flex flex-col items-center gap-2 group cursor-pointer relative z-10">
            <div class="absolute -top-8 bg-gray-800 text-white text-[10px] font-bold px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
              {{ semana.valor }} ordens
            </div>
            <div class="w-full max-w-[40px] bg-gradient-to-t from-blue-600 to-blue-400 rounded-t-lg transition-all duration-700 ease-out hover:from-blue-500 hover:to-blue-300 shadow-sm"
              :style="{ height: `${maxSemana > 0 ? (semana.valor / maxSemana) * 120 : 5}px` }"></div>
            <span class="text-[10px] font-bold text-gray-400 uppercase tracking-tighter text-center w-full truncate">{{ semana.label }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import api from '@/services/api'

const dadosBrutos = ref({
  totalOrdens: 0, abertas: 0, emExecucao: 0, concluidas: 0, tempo_medio: '0d',
  statusDetalhados: { ABERTA: 0, APROVADA: 0, EM_EXECUCAO: 0, AGUARDANDO_MATERIAL: 0, AGUARDANDO_TERCEIRO: 0, CONCLUIDA: 0, REPROVADA: 0, CANCELADA: 0, ENCERRADA: 0 },
  rankingTecnicos: [] as Array<{ nome: string; total: number; concluidas: number }>,
  pendencias: { aguardando_aprovacao: 0, aguardando_material: 0, aguardando_terceiro: 0, sem_tecnico: 0 },
  semanas: [] as Array<{ label: string; valor: number }>
})

const ordensPorStatus = computed(() => {
  const statusGeral = dadosBrutos.value?.statusDetalhados || {}
  return [
    { status: 'ABERTA', label: 'Pendentes de Triagem', quantidade: statusGeral.ABERTA || 0, corGradiente: 'bg-gradient-to-r from-blue-400 to-blue-500', corTexto: 'text-blue-600' },
    { status: 'APROVADA', label: 'Aprovadas pelos Gestores', quantidade: statusGeral.APROVADA || 0, corGradiente: 'bg-gradient-to-r from-emerald-400 to-emerald-500', corTexto: 'text-emerald-600' },
    { status: 'EM_EXECUCAO', label: 'Trabalho em Execução', quantidade: statusGeral.EM_EXECUCAO || 0, corGradiente: 'bg-gradient-to-r from-yellow-400 to-yellow-500', corTexto: 'text-yellow-600' },
    { status: 'AGUARDANDO_MATERIAL', label: 'Pausadas (Material/Terceiros)', quantidade: (statusGeral.AGUARDANDO_MATERIAL || 0) + (statusGeral.AGUARDANDO_TERCEIRO || 0), corGradiente: 'bg-gradient-to-r from-orange-400 to-orange-500', corTexto: 'text-orange-600' },
    { status: 'CONCLUIDA', label: 'Sucesso (Concluídas)', quantidade: (statusGeral.CONCLUIDA || 0) + (statusGeral.ENCERRADA || 0), corGradiente: 'bg-gradient-to-r from-teal-400 to-teal-500', corTexto: 'text-teal-600' },
    { status: 'CANCELADA', label: 'Canceladas / Reprovadas', quantidade: (statusGeral.CANCELADA || 0) + (statusGeral.REPROVADA || 0), corGradiente: 'bg-gradient-to-r from-red-400 to-red-500', corTexto: 'text-red-600' },
  ]
})

const tecnicos = computed(() => dadosBrutos.value?.rankingTecnicos || [])

const pendentes = computed(() => {
  const p = dadosBrutos.value?.pendencias || { aguardando_aprovacao: 0, aguardando_material: 0, aguardando_terceiro: 0, sem_tecnico: 0 }
  return [
    { label: 'Totens sem triagem dos Gestores', valor: p.aguardando_aprovacao || 0, cor: 'text-orange-600', bgCor: 'bg-orange-50' },
    { label: 'Estoque faltante (Material)', valor: p.aguardando_material || 0, cor: 'text-yellow-600', bgCor: 'bg-yellow-50' },
    { label: 'Serviços terceirizados pendentes', valor: p.aguardando_terceiro || 0, cor: 'text-purple-600', bgCor: 'bg-purple-50' },
    { label: 'Ordens aprovadas mas sem equipe', valor: p.sem_tecnico || 0, cor: 'text-red-600', bgCor: 'bg-red-50' },
  ]
})

const semanas = computed(() => {
  return dadosBrutos.value?.semanas?.length ? dadosBrutos.value.semanas : [
    { label: 'Sem 1', valor: 0 }, { label: 'Sem 2', valor: 0 }, { label: 'Sem 3', valor: 0 },
    { label: 'Sem 4', valor: 0 }, { label: 'Sem 5', valor: 0 }, { label: 'Sem 6', valor: 0 }
  ]
})
const maxSemana = computed(() => Math.max(...semanas.value.map(s => s.valor), 0))

async function buscarDadosDashboard() {
  try {
    const token = localStorage.getItem('token')
    const response = await api.get('/ordem-servico/dashboard/indicadores/', { headers: { Authorization: `Bearer ${token}` } })
    const dadosApi = response.data?.dados || response.data || {}
    
    dadosBrutos.value = {
      totalOrdens: dadosApi.totalOrdens || 0, abertas: dadosApi.abertas || 0, emExecucao: dadosApi.emExecucao || 0, concluidas: dadosApi.concluidas || 0, tempo_medio: dadosApi.tempo_medio || '0d',
      statusDetalhados: {
        ABERTA: dadosApi.statusDetalhados?.ABERTA || 0, APROVADA: dadosApi.statusDetalhados?.APROVADA || 0, EM_EXECUCAO: dadosApi.statusDetalhados?.EM_EXECUCAO || 0,
        AGUARDANDO_MATERIAL: dadosApi.statusDetalhados?.AGUARDANDO_MATERIAL || 0, AGUARDANDO_TERCEIRO: dadosApi.statusDetalhados?.AGUARDANDO_TERCEIRO || 0,
        CONCLUIDA: dadosApi.statusDetalhados?.CONCLUIDA || 0, REPROVADA: dadosApi.statusDetalhados?.REPROVADA || 0, CANCELADA: dadosApi.statusDetalhados?.CANCELADA || 0, ENCERRADA: dadosApi.statusDetalhados?.ENCERRADA || 0,
      },
      rankingTecnicos: dadosApi.rankingTecnicos || [],
      pendencias: dadosApi.pendencias || { aguardando_aprovacao: 0, aguardando_material: 0, aguardando_terceiro: 0, sem_tecnico: 0 },
      semanas: dadosApi.semanas || []
    }
  } catch (e) { console.error('Erro ao buscar dados do dashboard Gerente:', e) }
}

onMounted(() => buscarDadosDashboard())
</script>