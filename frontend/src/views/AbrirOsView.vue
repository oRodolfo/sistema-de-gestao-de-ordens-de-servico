<template>
    <div class="min-h-screen h-screen flex relative">

        <!-- Painel esquerdo azul -->
        <div class="w-3/8 bg-blue-800 flex flex-col items-center justify-center gap-6">
            <img src="@/assets/img/fho.png" alt="Logo da FHO" class="w-24 h-24 object-contain" />
            <div class="text-center">
                <h1 class="text-white text-2xl font-bold">Fundação Hermínio Ometto</h1>
                <p class="text-blue-200 text-sm mt-2">Abertura de Ordem de Serviço</p>
            </div>
        </div>

        <!-- Painel direito branco -->
        <div class="flex-1 flex flex-col items-center justify-center h-full overflow-y-auto py-8">
            <div class="w-full max-w-md px-8">
                <h2 class="text-blue-800 text-2xl font-bold mb-1">Nova OS</h2>
                <p class="text-gray-400 text-sm mb-6">Preencha os dados da ocorrencia</p>

                <!-- Seleção de tipo de usuário -->
                <div class="flex gap-6 mb-6">
                    <button type="button" @click="tipoUsuario = 'aluno'" :class="[
                        'flex-1 py-3 px-3 rounded-lg font-semibold border cursor-pointer',
                        tipoUsuario === 'aluno'
                            ? 'bg-blue-800 text-white border-blue-800'
                            : 'bg-white text-blue-800 border-blue-800 hover:bg-blue-50'
                    ]">
                        Aluno
                    </button>

                    <button type="button" @click="tipoUsuario = 'funcionario'" :class="[
                        'flex-1 py-3 px-3 rounded-lg font-semibold border cursor-pointer',
                        tipoUsuario === 'funcionario'
                            ? 'bg-blue-800 text-white border-blue-800'
                            : 'bg-white text-blue-800 border-blue-800 hover:bg-blue-50'
                    ]">
                        Funcionario
                    </button>

                </div>

                <!-- Campo de identificação -->
                <div v-if="tipoUsuario" class="flex flex-col gap-1 mt-4">
                    <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">
                        {{ tipoUsuario === 'aluno' ? 'RA - Registro do Aluno' : 'F - Número do Funcionário' }}
                    </label>
                    <input v-model="indentificacao" type="text"
                        :placeholder="tipoUsuario === 'aluno' ? 'Ex: 123456' : 'Ex: F1234'"
                        class="border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-blue-600 w-full" />
                </div>

                <!-- Campo de local -->
                <div v-if="tipoUsuario" class="flex flex-col gap-1 mt-4">
                    <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">
                        Local
                    </label>
                    <select v-model="local"
                        class="border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-blue-600 w-full cursor-pointer">
                        <option value="">Selecione o Local</option>
                        <option value="bosque-cima">Bosque de Cima</option>
                        <option value="bosque-baixo">Bosque de Baixo</option>
                        <option value="piscina">Piscina</option>
                        <option value="quadra-aberta">Quadra Aberta</option>
                        <option value="quadra-fechada">Quadra Fechada</option>
                        <option value="ginasio">Ginásio</option>
                        <option value="campo">Campo</option>
                        <option value="bloco">Bloco</option>
                    </select>

                    <!-- Campo de especificação do local -->
                     <div v-if="local" class="flex flex-col gap-1 mt-4">
                        <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">
                            Especifique o local
                        </label>
                        <input 
                            v-model="especificacao"
                            type="text"
                            placeholder="Ex: Sala 10, Cantina, Corredor"
                            class="border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-blue-600 w-full"
                        />
                     </div>

                     <!-- Campo de observação -->
                      <div v-if="local" class="flex flex-col gap-1 mt-4">
                        <label class="text-sm font-semibold text-gray-600 uppercase tracking-wide">
                            Observação / Descrição do problema
                        </label>
                        <textarea
                            v-model="observacao"
                            placeholder="Ex: Arrumar ar condicionado, projetor, cadeira..."
                            rows="3"
                            class="border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-blue-600 w-full resize-none"
                        >
                        </textarea>
                      </div>

                      <!-- Botões de ação -->
                       <div class="flex gap-3 mt-06">
                        <button
                            type="button"
                            @click="router.push('/')"
                            class="flex-1 py-3 rounded-lg border border-blue-800 text-blue-800 font-semibold hover:bg-blue-50 cursor-pointer"
                        >
                            Voltar
                        </button>

                        <button
                            type="button"
                            @click="enviarOS"
                            class="flex-1 py-3 rounded-lg  bg-blue-800 text-white font-semibold hover:bg-blue-600 cursor-pointer"
                        >
                            Enviar OS
                        </button>
                       </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script setup lang="ts">

import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const tipoUsuario = ref('')

const indentificacao = ref('')
const local = ref('')
const especificacao = ref('')
const observacao = ref('')

const carregando = ref(false)
const erro = ref('')

function enviarOS() {
    console.log({
        tipoUsuario: tipoUsuario.value,
        indentificacao: indentificacao.value,
        local: local.value,
        especificacao: especificacao.value,
        observacao: observacao.value
    })
}
</script>