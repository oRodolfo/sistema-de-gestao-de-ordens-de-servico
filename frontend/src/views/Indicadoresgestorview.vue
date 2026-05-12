<template>
  <div class="p-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-800">Indicadores</h1>
      <p class="text-sm text-gray-500 mt-1">Acompanhe o desempenho das ordens sob sua gestão</p>
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
        <h2 class="text-base font-bold text-gray-800 mb-4">Ordens por Status</h2>
        <div class="space-y-3">
          <div v-for="item in ordensPorStatus" :key="item.status" class="flex items-center gap-3">
            <span class="w-32 text-xs text-gray-600 shrink-0">{{ item.label }}</span>
            <div class="flex-1 bg-gray-100 rounded-full h-3">
              <div class="h-3 rounded-full transition-all" :class="item.cor"
                :style="{ width: `${(item.quantidade / totalOrdens) * 100}%` }"></div>
            </div>
            <span class="text-xs font-bold text-gray-700 w-6 text-right">{{ item.quantidade }}</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 class="text-base font-bold text-gray-800 mb-4">Técnicos com Mais Ordens</h2>
        <div class="space-y-3">
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
        <h2 class="text-base font-bold text-gray-800 mb-4">Ordens Pendentes de Ação</h2>
        <div class="space-y-3">
          <div v-for="item in pendentes" :key="item.label" class="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
            <span class="text-sm text-gray-600">{{ item.label }}</span>
            <span class="text-sm font-bold" :class="item.cor">{{ item.valor }}</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 class="text-base font-bold text-gray-800 mb-4">Ordens Concluídas por Semana</h2>
        <div class="flex items-end gap-3 h-32">
          <div v-for="semana in semanas" :key="semana.label" class="flex-1 flex flex-col items-center gap-1">
            <span class="text-xs font-bold text-gray-600">{{ semana.valor }}</span>
            <div class="w-full bg-blue-500 rounded-t-md transition-all"
              :style="{ height: `${(semana.valor / maxSemana) * 96}px` }"></div>
            <span class="text-xs text-gray-400">{{ semana.label }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const cards = [
  { label: 'Total sob Gestão', valor: 18, cor: 'text-blue-700', descricao: 'ordens atribuídas' },
  { label: 'Aguard. Aprovação', valor: 5, cor: 'text-orange-500', descricao: 'requerem ação' },
  { label: 'Em Execução', valor: 4, cor: 'text-yellow-500', descricao: 'sendo atendidas' },
  { label: 'Concluídas', valor: 9, cor: 'text-green-600', descricao: 'finalizadas' },
]

const ordensPorStatus = [
  { status: 'ABERTA', label: 'Abertas', quantidade: 5, cor: 'bg-blue-400' },
  { status: 'APROVADA', label: 'Aprovadas', quantidade: 3, cor: 'bg-green-400' },
  { status: 'EM_EXECUCAO', label: 'Em Execução', quantidade: 4, cor: 'bg-yellow-400' },
  { status: 'AGUARDANDO_MATERIAL', label: 'Aguard. Material', quantidade: 2, cor: 'bg-orange-400' },
  { status: 'CONCLUIDA', label: 'Concluídas', quantidade: 9, cor: 'bg-teal-400' },
  { status: 'REPROVADA', label: 'Reprovadas', quantidade: 1, cor: 'bg-red-400' },
]

const totalOrdens = computed(() => ordensPorStatus.reduce((acc, i) => acc + i.quantidade, 0))

const tecnicos = [
  { nome: 'Carlos Técnico', total: 8, concluidas: 6 },
  { nome: 'Roberto Técnico', total: 5, concluidas: 4 },
  { nome: 'Ana Técnica', total: 3, concluidas: 2 },
]

const pendentes = [
  { label: 'Aguardando aprovação', valor: 5, cor: 'text-orange-500' },
  { label: 'Aguardando material', valor: 2, cor: 'text-yellow-600' },
  { label: 'Aguardando terceiro', valor: 1, cor: 'text-purple-600' },
  { label: 'Sem técnico atribuído', valor: 3, cor: 'text-red-500' },
]

const semanas = [
  { label: 'Sem 1', valor: 2 },
  { label: 'Sem 2', valor: 3 },
  { label: 'Sem 3', valor: 1 },
  { label: 'Sem 4', valor: 4 },
  { label: 'Sem 5', valor: 2 },
  { label: 'Sem 6', valor: 5 },
]

const maxSemana = computed(() => Math.max(...semanas.map(s => s.valor)))
</script>