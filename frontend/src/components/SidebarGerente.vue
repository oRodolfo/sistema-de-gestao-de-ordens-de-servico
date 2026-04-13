<template>
  <div class="w-64 h-screen bg-blue-800 flex flex-col">
    <div class="p-6 flex flex-col items-center gap-3 border-b border-blue-700">
      <img src="@/assets/img/fho.png" alt="Logo FHO" class="w-16 h-16 object-contain" />
      <div class="text-center">
        <p class="text-white text-sm font-bold">Fundação Hermínio Ometto</p>
        <p class="text-blue-300 text-sm mt-1">Painel do Gerente</p>
      </div>
    </div>

    <nav class="flex-1 p-4 flex flex-col gap-1">

      <button @click="router.push('/dashboard-gerente/funcionarios')"
        class="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-blue-100 hover:bg-blue-700 cursor-pointer">
        <span>👥</span>
        <span>Funcionários</span>
      </button>

      <button @click="router.push('/dashboard-gerente/ordens')"
        class="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-blue-100 hover:bg-blue-700 cursor-pointer">
        <span>📋</span>
        <span>Ordens de Serviço</span>
      </button>

      <button @click="router.push('/dashboard-gerente/indicadores')"
        class="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-blue-100 hover:bg-blue-700 cursor-pointer">
        <span>📊</span>
        <span>Indicadores</span>
      </button>
    </nav>

    <div class="p-4 border-t border-blue-700">
      <button @click="fazerLogout"
        class="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-red-300 hover:bg-red-600 hover:text-white cursor-pointer">
        <span>🚪</span>
        <span>Sair</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">

import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

function fazerLogout() {
  authStore.logout()
  router.push('/')
}
</script>