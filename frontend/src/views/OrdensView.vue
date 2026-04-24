<template>
  <div class="p-8">

    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Ordens de Serviço</h1>
    </div>

    <div v-if="carregando" class="text-center text-gray-400 py-12">
      Carregando...
    </div>

    <div v-else-if="ordens.length === 0" class="text-center text-gray-400 py-12">
      Nenhuma ordem de serviço encontrada.
    </div>

    <!-- Tabela -->
    <div v-else class="bg-white rounded-lg shadow-sm overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">#</th>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Local</th>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Status</th>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Prioridade</th>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Data Abertura
            </th>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="ordem in ordens" :key="ordem.id_ordem_servico" class="hover:bg-gray-50">
            <td class="px-6 py-4 text-sm text-gray-800">#{{ ordem.id_ordem_servico }}</td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ ordem.localizacao }}</td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ ordem.status }}</td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ ordem.prioridade }}</td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ ordem.dt_abertura }}</td>
            <td class="px-6 py-4 text-sm flex gap-2">
              <button class="text-blue-600 hover:text-blue-800 cursor-pointer">Ver</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const ordens = ref<any[]>([])
const carregando = ref(false)

onMounted(async () => {
  carregando.value = true
  const resposta = await api.get('/ordens/')
  ordens.value = resposta.data
  carregando.value = false
})
</script>