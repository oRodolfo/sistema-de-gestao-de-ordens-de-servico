<template>
    <div class="min-h-screen h-screen flex relative">
        <!-- Painel Azul -->
        <div class="w-3/8 bg-blue-800 flex flex-col items-center justify-center gap-6">
            <img src="@/assets/img/fho.png" alt="Logo da FHO" class="w-24 h-24 object-contain">
            <div class="text-center">
                <h1 class="text-white text-2xl font-bold">Fundação Hermínio Ometto</h1>
                <p class="text-blue-200 text-sm mt-2">Cadastro de Usuarios</p>
            </div>
        </div>

        <!-- TOAST -->
         <div v-if="erro" class="absolute top-4 left-0 right-0 flex justify-center z-50">
            <div class="bg-red-500 text-white px-5 py-4 rounded-lg flex items-center gap-3">
                <span>X</span>
                <p class="text-sm font-medium">{{ erro }}</p>

            </div>
         </div>

        <!-- Painel Branco -->
        <div class="flex-1 flex flex-col items-center justify-center">
            <div class="w-full max-w-md px-8">
                <h2 class="text-blue-800 text-2xl font-bold mb-1">Cadastro de Usuarios</h2>
                <p class="text-gray-400 text-sm mb-6">Preencha os dados pra solicitar acesso</p>

                <form @submit.prevent="cadastrar" class="flex flex-col gap-4">

                    <!--Campos-->
                    <div>
                        <label class="text-sm font-semibold text-gray-600 uppercase tracking-wide">Nome</label>
                        <input v-model="nome" type="text" placeholder="Nome Completo"
                            class="border border-gray-300 rounded-lg px-4 text-sm outline-none focus:border-blue-600 w-full">
                    </div>

                    <div>
                        <label class="text-sm font-semibold text-gray-600 uppercase tracking-wide">Email</label>
                        <input v-model="email" type="email" placeholder="Usuario@fho.edu.br"
                            class="border border-gray-300 rounded-lg px-4 text-sm outline-none focus:border-blue-600 w-full">
                    </div>

                    <div>
                        <label class="text-sm font-semibold text-gray-600 uppercase tracking-wide">Senha</label>
                        <input v-model="senha" type="password" placeholder="***********"
                            class="border border-gray-300 rounded-lg px-4 text-sm outline-none focus:border-blue-600 w-full">
                    </div>

                    <div class="flex flex-col gap-1 mt-4">
                        <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">
                            Cargo do Usuario
                        </label>
                        <select v-model="tipo"
                            class="border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-blue-600 w-full cursor-pointer">
                            <option value="">Escolha a função do usuario</option>
                            <option value="gerente">Gerente</option>
                            <option value="gestor">Gestor</option>
                            <option value="tecnico">Técnico</option>
                        </select>
                    </div>

                    <!-- Botões de ação -->
                    <div class="flex gap-3 mt-6">
                        <button type="button" @click="router.push('/')"
                            class="flex-1 py-3 rounded-lg border border-blue-800 text-blue-800 font-semibold hover:bg-blue-50 cursor-pointer">
                            Voltar
                        </button>

                        <button type="submit"
                            class="flex-1 py-3 rounded-lg bg-blue-800 text-white font-semibold hover:bg-blue-600 cursor-pointer">
                            Cadastrar
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()

const nome = ref('')
const email = ref('')
const senha = ref('')
const tipo = ref('')
const carregando = ref(false)
const erro = ref('')
const sucesso = ref(false)

async function cadastrar() {
    carregando.value = true
    erro.value = ''

    try {
        await api.post('/usuarios/', {
            nome: nome.value,
            email: email.value,
            senha: senha.value,
            tipo: tipo.value
        })

        sucesso.value = true
        setTimeout(() => router.push('/'), 2000)
    } catch (e) {
        erro.value = "Erro ao cadastrar. Verifique os dados e tente novamente."
        setTimeout(() => { erro.value = '' }, 3000)
    } finally {
        carregando.value = false
    }
}

</script>

