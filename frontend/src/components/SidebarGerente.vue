<template>
  <div 
    @mouseenter="isExpanded = true" 
    @mouseleave="isExpanded = false"
    :class="[
      'h-full bg-[#1e3a8a] flex flex-col shrink-0 transition-all duration-300 ease-in-out z-50 shadow-xl relative border-r border-blue-800',
      isExpanded ? 'w-64' : 'w-20'
    ]"
  >
    <div class="h-24 flex items-center justify-start px-5 border-b border-blue-800/60">
      <img src="@/assets/img/fho.png" alt="Logo FHO" class="w-10 h-10 object-contain shrink-0 transition-transform duration-300" :class="isExpanded ? 'scale-105' : ''" />
      <div 
        class="ml-4 flex flex-col justify-center overflow-hidden whitespace-nowrap transition-all duration-300"
        :class="isExpanded ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-4 w-0'"
      >
        <p class="text-white text-sm font-extrabold tracking-wide">FHO</p>
        <p class="text-blue-300 text-[10px] uppercase font-semibold tracking-widest mt-0.5">Painel do Gerente</p>
      </div>
    </div>

    <nav class="flex-1 px-3 py-6 flex flex-col gap-1.5 overflow-x-hidden">
      <button @click="router.push('/dashboard-gerente/indicadores')"
        :class="[
          'flex items-center gap-4 px-3 py-3 rounded-xl cursor-pointer transition-all duration-200 group',
          route.path.includes('indicadores') ? 'bg-blue-600/50 text-white font-semibold shadow-inner' : 'text-blue-200 hover:bg-blue-800/50 hover:text-white'
        ]">
        <span class="text-xl w-8 text-center shrink-0">📊</span>
        <span class="text-sm whitespace-nowrap transition-all duration-300" :class="isExpanded ? 'opacity-100' : 'opacity-0 w-0'">Indicadores</span>
      </button>

      <button @click="router.push('/dashboard-gerente/funcionarios')"
        :class="[
          'flex items-center gap-4 px-3 py-3 rounded-xl cursor-pointer transition-all duration-200 group',
          route.path.includes('funcionarios') ? 'bg-blue-600/50 text-white font-semibold shadow-inner' : 'text-blue-200 hover:bg-blue-800/50 hover:text-white'
        ]">
        <span class="text-xl w-8 text-center shrink-0">👥</span>
        <span class="text-sm whitespace-nowrap transition-all duration-300" :class="isExpanded ? 'opacity-100' : 'opacity-0 w-0'">Funcionários</span>
      </button>

      <button @click="router.push('/dashboard-gerente/ordens')"
        :class="[
          'flex items-center gap-4 px-3 py-3 rounded-xl cursor-pointer transition-all duration-200 group',
          route.path.includes('ordens') ? 'bg-blue-600/50 text-white font-semibold shadow-inner' : 'text-blue-200 hover:bg-blue-800/50 hover:text-white'
        ]">
        <span class="text-xl w-8 text-center shrink-0">📋</span>
        <span class="text-sm whitespace-nowrap transition-all duration-300" :class="isExpanded ? 'opacity-100' : 'opacity-0 w-0'">Ordens de Serviço</span>
      </button>
    </nav>

    <div class="p-4 border-t border-blue-800/60">
      <div class="flex items-center bg-blue-900/40 border border-blue-800/50 rounded-2xl p-2 transition-all duration-300">
        <div class="w-10 h-10 rounded-full bg-gradient-to-tr from-blue-500 to-blue-400 flex items-center justify-center text-white text-sm font-bold shrink-0 shadow-md">
          {{ iniciaisUsuario }}
        </div>
        <div class="flex flex-col justify-center ml-3 overflow-hidden whitespace-nowrap transition-all duration-300" :class="isExpanded ? 'w-[100px] opacity-100' : 'w-0 opacity-0'">
          <p class="text-white text-xs font-semibold truncate">{{ nomeUsuario }}</p>
          <p class="text-blue-300 text-[10px] uppercase font-medium mt-0.5">Gerente</p>
        </div>
        <button v-if="isExpanded" @click="fazerLogout" title="Sair do sistema" class="ml-auto w-8 h-8 rounded-xl text-red-300 hover:bg-red-500 hover:text-white flex items-center justify-center transition-all duration-200">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Swal from 'sweetalert2'

const router = useRouter()
const authStore = useAuthStore()
const route = useRoute()
const isExpanded = ref(false)

const getUserData = () => {
  const storeUser = authStore.usuario as any
  if (storeUser && storeUser.nome) return storeUser
  const userStorage = localStorage.getItem('usuario')
  if (userStorage) {
    try { return JSON.parse(userStorage) } catch (e) { return null }
  }
  return null
}

const nomeUsuario = computed(() => {
  const user = getUserData()
  return user?.nome || user?.name || 'Usuário Logado'
})

const iniciaisUsuario = computed(() => {
  const nome = nomeUsuario.value
  if (nome === 'Usuário Logado') return 'US'
  return nome.substring(0, 2).toUpperCase()
})

function fazerLogout() {
  Swal.fire({
    title: 'Sair do Sistema?', text: "Você precisará fazer login novamente.", icon: 'question',
    showCancelButton: true, confirmButtonColor: '#2563eb', cancelButtonColor: '#dc2626', confirmButtonText: 'Sim, sair', cancelButtonText: 'Cancelar',
    customClass: { popup: 'rounded-2xl', confirmButton: 'rounded-xl px-4 py-2 font-semibold', cancelButton: 'rounded-xl px-4 py-2 font-semibold' }
  }).then((result) => {
    if (result.isConfirmed) { authStore.logout(); router.push('/') }
  })
}
</script>