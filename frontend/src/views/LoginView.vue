<template>
    <div class="min-h-screen h-screen flex">
        <div class="w-3/8 bg-blue-800 flex flex-col items-center justify-center">
            <img src="@/assets/img/fho.png" alt="Logo da FHO" class="w-24 h-24 object-contain" />

            <div class="text-center">
                <h1 class="text-white text-2xl font-bold">Fundação Hermínio Ometto</h1>
                <p class="text-blue-200 text-sm mt-2">Sistema de Ordem de Serviço</p>
            </div>
        </div>

        <!-- Formulário -->
        <div class="flex-1 flex flex-col items-center justify-center h-full">
            <div class="w-full max-w-md px-8">
                <h2 class="text-blue-800 text-2xl font-bold mb-1">Bem-vindos</h2>
                <p class="text-gray-400 text-sm mb-8">Acesse com suas credenciais institucionais</p>

                <!-- Campo email -->
                <form @submit.prevent="fazerLogin" class="flex flex-col gap-4">
                    <div class="flex flex-col gap-1">
                        <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Email</label>
                        <input 
                            v-model="email"
                            type="email"
                            placeholder="seu.email@fho.edu.br"
                            class="border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-blue-600"
                        />
                    </div>

                    <!-- Campo senha -->
                     <div class="flex flex-col gap-1">
                        <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Senha</label>
                        <input 
                            v-model="senha"
                            type="password"
                            placeholder="********"
                            class="border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-blue-600"
                        />
                     </div>

                     <!-- Botão -->
                      <button 
                        type="submit"
                        :disabled="carregando"
                        class="bg-blue-800 text-white py-3 rounded-lg font-semibold mt-2 hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {{carregando ? 'Entrando...' : 'Entrar'}}
                      </button>

                      <p v-if="erro" class="text-red-500 text-sm text-center">{{ erro }}</p>

                </form>

            </div>
            
        </div>
    </div>

    
    
</template>

<script setup lang="ts">
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'

    const router = useRouter()
    
    const email = ref('')
    const senha = ref('')
    const carregando = ref(false)
    const erro = ref('')

    function fazerLogin() {
        carregando.value = true
        erro.value = ''

        setTimeout(() => {
            carregando.value = false
            router.push('/dashboard')
        }, 2000);
        console.log(email.value, senha.value)
        //aqui vai a chamada pra API de login quando estiver pronta
    }

</script>

<style>

</style>