<template>
  <div class="p-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-800">Painel do Gestor</h1>
      <p class="text-sm text-gray-500 mt-1">Acompanhe as ordens sob sua supervisão e novos chamados</p>
    </div>

    <div class="grid grid-cols-2 gap-4 mb-8 lg:grid-cols-4">
      <div v-for="card in cards" :key="card.label" class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">{{ card.label }}</p>
        <p class="text-3xl font-bold" :class="card.cor">{{ card.valor }}</p>
        <p class="text-xs text-gray-400 mt-1">{{ card.descricao }}</p>
      </div>
    </div>

    <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 class="text-base font-bold text-gray-800 mb-4">Acompanhamento de Status</h2>
        <div class="space-y-3">
          <div v-for="item in ordensPorStatus" :key="item.status" class="flex items-center gap-3">
            <span class="w-32 text-xs text-gray-600 shrink-0">{{ item.label }}</span>
            <div class="flex-1 bg-gray-100 rounded-full h-3">
              <div class="h-3 rounded-full transition-all" :class="item.cor"
                :style="{ width: `${totalOrdens > 0 ? (item.quantidade / totalOrdens) * 100 : 0}%` }">
              </div>
            </div>
            <span class="text-xs font-bold text-gray-700 w-6 text-right">{{ item.quantidade || 0 }}</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 class="text-base font-bold text-gray-800 mb-4">Carga de Trabalho da Equipe</h2>
        <div class="space-y-3">
          <p v-if="!tecnicos.length" class="text-sm text-gray-400 text-center py-4">Nenhuma ordem atribuída aos técnicos.</p>
          <div v-for="(tec, index) in tecnicos" :key="tec.nome" class="flex items-center gap-4">
            <span class="text-lg font-bold text-gray-300 w-6">{{ index + 1 }}</span>
            <div class="flex-1">
              <p class="text-sm font-semibold text-gray-800">{{ tec.nome }}</p>
              <p class="text-xs text-gray-400">{{ tec.concluidas }} concluídas / {{ tec.total }} total</p>
            </div>
            <span class="text-sm font-bold text-blue-700">{{ tec.total }}</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 class="text-base font-bold text-gray-800 mb-4">Atenção Necessária</h2>
        <div class="space-y-3">
          <div v-for="item in pendentes" :key="item.label" class="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
            <span class="text-sm text-gray-600">{{ item.label }}</span>
            <span class="text-sm font-bold" :class="item.cor">{{ item.valor }}</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 class="text-base font-bold text-gray-800 mb-4">Conclusões Semanais</h2>
        <div class="flex items-end gap-3 h-32">
          <div v-for="semana in semanas" :key="semana.label" class="flex-1 flex flex-col items-center gap-1">
            <span class="text-xs font-bold text-gray-600">{{ semana.valor }}</span>
            <div class="w-full bg-blue-500 rounded-t-md transition-all"
              :style="{ height: `${maxSemana > 0 ? (semana.valor / maxSemana) * 96 : 0}px` }"></div>
            <span class="text-xs text-gray-400">{{ semana.label }}</span>
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
  totalOrdens: 0,
  abertas: 0,
  emExecucao: 0,
  concluidas: 0,
  statusDetalhados: {
    ABERTA: 0, APROVADA: 0, EM_EXECUCAO: 0,
    AGUARDANDO_MATERIAL: 0, AGUARDANDO_TERCEIRO: 0,
    CONCLUIDA: 0, REPROVADA: 0, CANCELADA: 0, ENCERRADA: 0
  },
  rankingTecnicos: [] as Array<{ nome: string; total: number; concluidas: number }>,
  pendencias: { aguardando_aprovacao: 0, aguardando_material: 0, aguardando_terceiro: 0, sem_tecnico: 0 },
  semanas: [] as Array<{ label: string; valor: number }>
})

const cards = computed(() => [
  { label: 'Total do Setor', valor: dadosBrutos.value?.totalOrdens || 0, cor: 'text-blue-700', descricao: 'ordens visíveis' },
  { label: 'Para Triagem', valor: dadosBrutos.value?.abertas || 0, cor: 'text-orange-500', descricao: 'precisam de técnico' },
  { label: 'Em Execução', valor: dadosBrutos.value?.emExecucao || 0, cor: 'text-yellow-500', descricao: 'sendo atendidas' },
  { label: 'Concluídas', valor: dadosBrutos.value?.concluidas || 0, cor: 'text-green-600', descricao: 'finalizadas' },
])

const ordensPorStatus = computed(() => {
  const statusGeral = dadosBrutos.value?.statusDetalhados || {}
  return [
    { status: 'ABERTA', label: 'Na Fila (Abertas)', quantidade: statusGeral.ABERTA || 0, cor: 'bg-blue-400' },
    { status: 'APROVADA', label: 'Aprovadas', quantidade: statusGeral.APROVADA || 0, cor: 'bg-green-400' },
    { status: 'EM_EXECUCAO', label: 'Em Execução', quantidade: statusGeral.EM_EXECUCAO || 0, cor: 'bg-yellow-400' },
    { status: 'AGUARDANDO_MATERIAL', label: 'Aguard. Material', quantidade: statusGeral.AGUARDANDO_MATERIAL || 0, cor: 'bg-orange-400' },
    { status: 'CONCLUIDA', label: 'Concluídas/Encerradas', quantidade: (statusGeral.CONCLUIDA || 0) + (statusGeral.ENCERRADA || 0), cor: 'bg-teal-400' },
    { status: 'CANCELADA', label: 'Canceladas', quantidade: statusGeral.CANCELADA || 0, cor: 'bg-red-400' },
  ]
})

const totalOrdens = computed(() => dadosBrutos.value?.totalOrdens || 0)
const tecnicos = computed(() => dadosBrutos.value?.rankingTecnicos || [])

const pendentes = computed(() => {
  const p = dadosBrutos.value?.pendencias || { aguardando_aprovacao: 0, aguardando_material: 0, aguardando_terceiro: 0, sem_tecnico: 0 }
  return [
    { label: 'Para aprovar / triar', valor: p.aguardando_aprovacao || 0, cor: 'text-orange-500' },
    { label: 'Falta de material', valor: p.aguardando_material || 0, cor: 'text-yellow-600' },
    { label: 'Bloqueado por terceiro', valor: p.aguardando_terceiro || 0, cor: 'text-purple-600' },
    { label: 'Técnico não atribuído', valor: p.sem_tecnico || 0, cor: 'text-red-500' },
  ]
})

const semanas = computed(() => {
  return dadosBrutos.value?.semanas?.length ? dadosBrutos.value.semanas : [
    { label: 'Sem 1', valor: 0 }, { label: 'Sem 2', valor: 0 }, { label: 'Sem 3', valor: 0 },
    { label: 'Sem 4', valor: 0 }, { label: 'Sem 5', valor: 0 }, { label: 'Sem 6', valor: 0 }
  ]
})

const maxSemana = computed(() => Math.max(...semanas.value.map(s => s.valor), 1))

async function buscarDadosDashboard() {
  try {
    const token = localStorage.getItem('token')
    
    // Aproveita o exato mesmo endpoint, pois o Django agora filtra sozinho!
    const response = await api.get('/ordem-servico/dashboard/indicadores/', {
      headers: { Authorization: `Bearer ${token}` }
    })

    const dadosApi = response.data?.dados || response.data || {}
    
    dadosBrutos.value = {
      totalOrdens: dadosApi.totalOrdens || 0,
      abertas: dadosApi.abertas || 0,
      emExecucao: dadosApi.emExecucao || 0,
      concluidas: dadosApi.concluidas || 0,
      statusDetalhados: {
        ABERTA: dadosApi.statusDetalhados?.ABERTA || 0,
        APROVADA: dadosApi.statusDetalhados?.APROVADA || 0,
        EM_EXECUCAO: dadosApi.statusDetalhados?.EM_EXECUCAO || 0,
        AGUARDANDO_MATERIAL: dadosApi.statusDetalhados?.AGUARDANDO_MATERIAL || 0,
        AGUARDANDO_TERCEIRO: dadosApi.statusDetalhados?.AGUARDANDO_TERCEIRO || 0,
        CONCLUIDA: dadosApi.statusDetalhados?.CONCLUIDA || 0,
        REPROVADA: dadosApi.statusDetalhados?.REPROVADA || 0,
        CANCELADA: dadosApi.statusDetalhados?.CANCELADA || 0,
        ENCERRADA: dadosApi.statusDetalhados?.ENCERRADA || 0,
      },
      rankingTecnicos: dadosApi.rankingTecnicos || [],
      pendencias: dadosApi.pendencias || { aguardando_aprovacao: 0, aguardando_material: 0, aguardando_terceiro: 0, sem_tecnico: 0 },
      semanas: dadosApi.semanas || []
    }
  } catch (e) {
    console.error('Erro ao buscar dados do dashboard Gestor:', e)
  }
}

onMounted(() => {
  buscarDadosDashboard()
})
</script>