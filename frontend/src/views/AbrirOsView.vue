<template>
  <div class="fixed inset-0 w-screen h-screen min-h-screen flex overflow-hidden bg-white select-none">

    <div class="hidden md:flex w-2/5 bg-blue-800 flex-col items-center justify-center gap-6 p-8 shrink-0">
      <img src="@/assets/img/fho.png" alt="Logo da FHO" class="w-24 h-24 object-contain" />
      <div class="text-center">
        <h1 class="text-white text-2xl font-bold tracking-wide">Fundação Hermínio Ometto</h1>
        <p class="text-blue-200 text-sm mt-2 opacity-90">Abertura de Ordem de Serviço</p>
      </div>
    </div>

    <div class="flex-1 h-full overflow-y-auto bg-white flex flex-col justify-start md:justify-center items-center px-6 py-12 sm:px-12">
      <div class="w-full max-w-md space-y-6 my-auto">
        
        <div>
          <h2 class="text-blue-800 text-2xl font-bold mb-1">Nova OS</h2>
          <p class="text-gray-400 text-sm">Preencha os dados da ocorrência</p>
        </div>

        <div v-if="erro" class="p-3 bg-red-100 text-red-700 text-sm rounded-lg border border-red-200">
          {{ erro }}
        </div>
        <div v-if="sucesso" class="p-3 bg-green-100 text-green-700 text-sm rounded-lg border border-green-200">
          {{ sucesso }}
        </div>

        <div class="grid grid-cols-2 gap-4">
          <button type="button" @click="tipoUsuario = 'aluno'" :class="[
            'py-3 px-4 rounded-lg font-semibold border transition-all duration-200 cursor-pointer text-center text-sm',
            tipoUsuario === 'aluno'
              ? 'bg-blue-800 text-white border-blue-800 shadow-sm'
              : 'bg-white text-blue-800 border-gray-300 hover:bg-gray-50'
          ]">
            Aluno
          </button>

          <button type="button" @click="tipoUsuario = 'funcionario'" :class="[
            'py-3 px-4 rounded-lg font-semibold border transition-all duration-200 cursor-pointer text-center text-sm',
            tipoUsuario === 'funcionario'
              ? 'bg-blue-800 text-white border-blue-800 shadow-sm'
              : 'bg-white text-blue-800 border-gray-300 hover:bg-gray-50'
          ]">
            Funcionário
          </button>
        </div>

        <div class="space-y-4">
          <div class="flex flex-col gap-1.5">
            <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">
              {{ tipoUsuario === 'aluno' ? 'RA - Registro do Aluno' : 'F - Número do Funcionário' }}
            </label>
            <input v-model="indentificacao" type="text"
              :placeholder="tipoUsuario === 'aluno' ? 'Ex: 123456' : 'Ex: F1234'"
              class="border border-gray-300 rounded-lg px-4 py-2.5 text-sm outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600 w-full transition-all" />
          </div>

          <div class="flex flex-col gap-1.5 relative">
            <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">
              Local (Prédio / Bloco)
            </label>
            
            <div 
              @click="toggleDropdown"
              class="border border-gray-300 rounded-lg px-4 py-2.5 text-sm outline-none w-full cursor-pointer bg-white flex justify-between items-center transition-all min-h-[42px]"
              :class="{'border-blue-600 ring-1 ring-blue-600': dropdownAberto}"
            >
              <span :class="localNomeSelecionado ? 'text-gray-800' : 'text-gray-400'">
                {{ localNomeSelecionado || 'Selecione o Prédio' }}
              </span>
              <svg class="w-4 h-4 text-gray-400 transition-transform" :class="{'rotate-180': dropdownAberto}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>

            <div 
              v-if="dropdownAberto" 
              class="absolute left-0 right-0 top-[calc(100%+4px)] bg-white border border-gray-200 rounded-lg shadow-lg z-50 max-h-48 overflow-y-auto"
            >
              <ul class="py-1">
                <li 
                  v-for="predio in listaPredios" 
                  :key="predio.id_predio"
                  @click="selecionarPredio(predio)"
                  class="px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-800 cursor-pointer transition-colors"
                >
                  {{ predio.nome_predio }}
                </li>
              </ul>
            </div>
          </div>

          <div v-if="idPredioSelecionado" class="space-y-4 pt-1">
            <div class="flex flex-col gap-1.5">
              <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                Especifique o local (Sala, Laboratório ou Ambiente)
              </label>
              <input v-model="especificacao" type="text" placeholder="Ex: Sala 10, Laboratório 3, Cantina"
                class="border border-gray-300 rounded-lg px-4 py-2.5 text-sm outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600 w-full transition-all" />
            </div>

            <div class="flex flex-col gap-1.5">
              <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                Observação / Descrição do problema
              </label>
              <textarea v-model="observacao" placeholder="Ex: Arrumar ar condicionado, projetor queimado, cadeira quebrada..."
                rows="3"
                class="border border-gray-300 rounded-lg px-4 py-2.5 text-sm outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600 w-full resize-none transition-all">
              </textarea>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4 pt-2">
          <button type="button" @click="router.push('/')"
            class="py-3 rounded-lg border border-blue-800 text-blue-800 font-semibold hover:bg-blue-50 transition-all cursor-pointer text-center text-sm">
            Voltar
          </button>

          <button type="button" @click="enviarOS" :disabled="carregando"
            class="py-3 rounded-lg bg-blue-800 text-white font-semibold hover:bg-blue-700 transition-all cursor-pointer text-center text-sm disabled:bg-gray-400 disabled:cursor-not-allowed shadow-sm">
            {{ carregando ? 'Enviando...' : 'Enviar OS' }}
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

interface Predio {
  id_predio: number
  nome_predio: string
}

interface Localizacao {
  id_localizacao: number
  desc_localizacao: string
  predio: number
}

const router = useRouter()

const tipoUsuario = ref('aluno')
const indentificacao = ref('')
const idPredioSelecionado = ref<number | null>(null)
const localNomeSelecionado = ref('')
const dropdownAberto = ref(false)
const especificacao = ref('')
const observacao = ref('')

const carregando = ref(false)
const erro = ref('')
const sucesso = ref('')

const listaPredios = ref<Predio[]>([])
const listaLocalizacoes = ref<Localizacao[]>([])

function toggleDropdown() {
  dropdownAberto.value = !dropdownAberto.value
}

function selecionarPredio(predio: Predio) {
  idPredioSelecionado.value = predio.id_predio
  localNomeSelecionado.value = predio.nome_predio
  dropdownAberto.value = false
}

async function inicializarDados() {
  try {
    // 1. Carrega os Prédios para exibir as opções corretas (Ex: BLOCO A, BLOCO B...)
    const resPredios = await api.get('/predio/')
    listaPredios.value = resPredios.data.dados || resPredios.data

    // 2. Carrega as localizações em segundo plano para podermos buscar uma PK válida na hora do envio
    const resLoc = await api.get('/localizacao/')
    listaLocalizacoes.value = resLoc.data.dados || resLoc.data
  } catch (e) {
    console.error('Erro ao buscar dados iniciais:', e)
  }
}

async function enviarOS() {
  if (!indentificacao.value || !idPredioSelecionado.value || !observacao.value) {
    erro.value = 'Por favor, preencha todos os campos obrigatórios.'
    return
  }

  // Procura uma PK de localização correspondente a esse prédio no banco de dados para satisfazer o Django
  const localizacaoCorrespondente = listaLocalizacoes.value.find(
    l => l.predio === idPredioSelecionado.value
  )

  if (!localizacaoCorrespondente) {
    erro.value = 'Não encontramos um mapeamento válido para este prédio no sistema.'
    return
  }

  try {
    carregando.value = true
    erro.value = ''
    sucesso.value = ''

    const payload = {
      // Envia o id_localizacao numérico válido que o Django exige
      localizacao: localizacaoCorrespondente.id_localizacao, 
      
      // Concatena as strings para salvar o texto digitado pelo usuário perfeitamente
      descricao_servico: `[${tipoUsuario.value.toUpperCase()}: ${indentificacao.value}] - Local: ${localNomeSelecionado.value} (${especificacao.value}) - Problema: ${observacao.value}`,
      prioridade_urgencia: 'NAO'
    }

    await api.post('/ordem-servico/', payload)

    sucesso.value = 'Ordem de serviço aberta com sucesso!'

    indentificacao.value = ''
    idPredioSelecionado.value = null
    localNomeSelecionado.value = ''
    especificacao.value = ''
    observacao.value = ''

    setTimeout(() => {
      router.push('/')
    }, 2000)

  } catch (e: any) {
    console.error('Erro ao abrir OS:', e)
    if (e.response && e.response.data && e.response.data.msg) {
      erro.value = e.response.data.msg
    } else {
      erro.value = 'Falha ao conectar com o servidor. Tente novamente.'
    }
  } finally {
    carregando.value = false
  }
}

import { onMounted } from 'vue'

onMounted(() => {
  localStorage.removeItem('token') 
  inicializarDados() 
})
</script>