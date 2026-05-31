<template>
  <div class="p-8">
    <div class="mb-8 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">Gestão de Ativos</h1>
        <p class="text-sm text-gray-500 mt-1">Registe e gira os equipamentos da instituição para manutenções preventivas</p>
      </div>
      
      <div class="flex items-center gap-4 w-full md:w-auto">
        <div class="relative w-full md:w-72 lg:w-80">
          <span class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-gray-400 text-sm">🔍</span>
          <input v-model="termoBusca" type="text" placeholder="Buscar por código, marca, modelo..." class="w-full bg-white border border-gray-200 text-gray-700 placeholder-gray-400 text-sm rounded-lg pl-9 pr-3 py-2.5 outline-none focus:ring-2 focus:ring-blue-500 shadow-sm transition-all cursor-text" />
        </div>
        
        <button @click="abrirModalNovo" class="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold rounded-lg shadow-md transition-colors cursor-pointer flex items-center gap-2 shrink-0">
          <span>+</span> Novo Ativo
        </button>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-gray-50 border-b border-gray-100 text-xs text-gray-500 uppercase tracking-wider">
            <th class="p-4 font-semibold">Equipamento</th>
            <th class="p-4 font-semibold">Identificação</th>
            <th class="p-4 font-semibold">Preventiva</th>
            <th class="p-4 font-semibold">Localização</th>
            <th class="p-4 font-semibold text-center">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading" class="border-b border-gray-50"><td colspan="5" class="p-8 text-center text-gray-400 font-medium">A carregar ativos...</td></tr>
          <tr v-else-if="ativosFiltrados.length === 0" class="border-b border-gray-50"><td colspan="5" class="p-8 text-center text-gray-400 font-medium">Nenhum ativo encontrado.</td></tr>
          <tr v-else v-for="ativo in ativosFiltrados" :key="ativo.id_ativo || ativo.id" class="border-b border-gray-50 hover:bg-gray-50/80 transition-colors">
            
            <td class="p-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600 shrink-0">
                  <span v-if="ativo.tipo_ativo === 'AR_CONDICIONADO'" class="text-xl">❄️</span>
                  <span v-else class="text-xl">🖥️</span>
                </div>
                <div>
                  <div class="text-sm font-bold text-gray-800">{{ ativo.marca }} {{ ativo.modelo }}</div>
                  <div class="text-xs text-gray-500 mt-0.5">{{ formatarTipo(ativo.tipo_ativo) }}</div>
                </div>
              </div>
            </td>

            <td class="p-4">
              <div class="flex flex-col gap-1">
                <span class="px-2 py-0.5 bg-gray-100 text-gray-700 rounded text-[10px] font-bold tracking-wider border border-gray-200 w-fit">
                  PAT: {{ ativo.codigo_patrimonial || 'N/I' }}
                </span>
                <span class="text-xs text-gray-400 font-medium">SN: {{ ativo.numero_serial || 'N/I' }}</span>
              </div>
            </td>

            <td class="p-4">
              <div class="text-sm font-medium text-gray-700">A cada {{ ativo.periodicidade_preventiva_dias }} dias</div>
              <div class="text-[11px] text-gray-500 mt-0.5" v-if="ativo.dt_proxima_preventiva">
                Próxima: <span class="font-bold text-orange-500">{{ formatarData(ativo.dt_proxima_preventiva) }}</span>
              </div>
              <div class="text-[11px] text-gray-400 mt-0.5" v-else>
                Última: {{ formatarData(ativo.dt_ultima_preventiva) || 'Sem registo' }}
              </div>
            </td>

            <td class="p-4">
               <div class="flex items-center gap-2">
                 <span class="text-gray-400">📍</span>
                 <span class="text-sm font-medium text-gray-600">
                   {{ gerarNomeLocalizacao(ativo) }}
                 </span>
               </div>
            </td>

            <td class="p-4 text-center">
              <button @click="abrirModalEdicao(ativo)" class="text-blue-600 hover:text-white hover:bg-blue-600 font-bold border border-blue-200 px-3 py-1.5 rounded-lg transition-all shadow-sm cursor-pointer mr-2">Editar</button>
              <button @click="excluirAtivo(ativo.id_ativo || ativo.id)" class="text-red-600 hover:text-white hover:bg-red-600 font-bold border border-red-200 px-3 py-1.5 rounded-lg transition-all shadow-sm cursor-pointer">Remover</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="modalAberto" @click.self="fecharModal" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4 animate-fade-in">
      <div class="bg-white rounded-2xl w-full max-w-2xl overflow-hidden shadow-2xl flex flex-col">
        <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
          <div>
            <h2 class="text-xl font-bold text-gray-800">{{ modoEdicao ? 'Editar Ativo' : 'Registar Novo Ativo' }}</h2>
          </div>
          <button @click="fecharModal" class="text-gray-400 hover:text-gray-700 p-2 rounded-full hover:bg-gray-200 transition-colors cursor-pointer"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg></button>
        </div>
        
        <div class="p-6 space-y-5 overflow-y-auto max-h-[70vh]">
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="space-y-1.5">
              <label class="text-xs font-bold text-gray-500 uppercase tracking-wider">Tipo de Ativo *</label>
              <select v-model="form.tipo_ativo" class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm outline-none focus:bg-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 cursor-pointer">
                <option value="AR_CONDICIONADO">Ar Condicionado</option>
              </select>
            </div>
            
            <div class="space-y-1.5">
              <label class="text-xs font-bold text-gray-500 uppercase tracking-wider">Código Patrimonial *</label>
              <input v-model="form.codigo_patrimonial" type="text" placeholder="Ex: 63270" class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm outline-none focus:bg-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all" />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="space-y-1.5">
              <label class="text-xs font-bold text-gray-500 uppercase tracking-wider">Marca *</label>
              <input v-model="form.marca" type="text" placeholder="Ex: LG, Carrier" class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm outline-none focus:bg-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all" />
            </div>
            
            <div class="space-y-1.5">
              <label class="text-xs font-bold text-gray-500 uppercase tracking-wider">Modelo *</label>
              <input v-model="form.modelo" type="text" placeholder="Ex: Dual Inverter 12000" class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm outline-none focus:bg-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all" />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="space-y-1.5">
              <label class="text-xs font-bold text-gray-500 uppercase tracking-wider">Número Serial</label>
              <input v-model="form.numero_serial" type="text" placeholder="Ex: 4318B14346431" class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm outline-none focus:bg-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all" />
            </div>
            
            <div class="space-y-1.5">
              <label class="text-xs font-bold text-gray-500 uppercase tracking-wider">Preventiva (Dias) *</label>
              <input v-model.number="form.periodicidade_preventiva_dias" type="number" min="0" placeholder="Ex: 30" class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm outline-none focus:bg-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all" />
            </div>
          </div>

          <hr class="border-gray-100 my-2" />

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="space-y-1.5">
              <label class="text-xs font-bold text-gray-500 uppercase tracking-wider">Prédio / Bloco *</label>
              <select v-model="idPredioSelecionado" @change="aoTrocarPredio" class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm outline-none focus:bg-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 cursor-pointer">
                <option :value="null" disabled>Selecione o Prédio...</option>
                <option v-for="predio in listaPredios" :key="predio.id_predio || predio.id" :value="predio.id_predio || predio.id">{{ predio.nome_predio || predio.nome }}</option>
              </select>
            </div>

            <div class="space-y-1.5" v-if="idPredioSelecionado">
              <label class="text-xs font-bold text-gray-500 uppercase tracking-wider">Sala / Localização Exata *</label>
              <select v-model="form.id_localizacao" class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm outline-none focus:bg-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 cursor-pointer">
                <option value="" disabled>Selecione o ambiente...</option>
                <option v-for="loc in localizacoesFiltradas" :key="loc.id_localizacao || loc.id" :value="loc.id_localizacao || loc.id">{{ loc.desc_localizacao || loc.nome }}</option>
              </select>
            </div>
          </div>

        </div>
        
        <div class="p-6 border-t border-gray-100 flex justify-end gap-3 bg-gray-50">
          <button @click="fecharModal" class="px-6 py-2.5 rounded-lg font-bold text-gray-600 hover:bg-gray-200 transition-colors cursor-pointer">Cancelar</button>
          <button @click="salvarAtivo" :disabled="salvando" class="px-6 py-2.5 rounded-lg font-bold text-white bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 transition-colors cursor-pointer shadow-md">
            {{ salvando ? 'A guardar...' : 'Guardar Ativo' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import Swal from 'sweetalert2'

const ativos = ref<any[]>([])
const loading = ref(true)
const termoBusca = ref('')

const modalAberto = ref(false)
const modoEdicao = ref(false)
const salvando = ref(false)

const listaPredios = ref<any[]>([])
const listaLocalizacoes = ref<any[]>([])
const idPredioSelecionado = ref<number | null>(null)

const form = ref({
  id_ativo: null,
  codigo_patrimonial: '',
  tipo_ativo: 'AR_CONDICIONADO',
  marca: '',
  modelo: '',
  numero_serial: '',
  periodicidade_preventiva_dias: 30,
  id_localizacao: '' as number | string
})

const authHeader = () => {
  const token = localStorage.getItem('token')
  return { headers: { Authorization: `Bearer ${token}` } }
}

const formatarTipo = (tipo: string) => {
  if (!tipo) return 'Equipamento'
  return tipo.replace(/_/g, ' ')
}

const formatarData = (data: string) => {
  if (!data) return ''
  return new Date(data).toLocaleDateString('pt-BR')
}

const gerarNomeLocalizacao = (ativo: any) => {
  const locId = ativo.localizacao || ativo.id_localizacao || ativo.localizacao_id;
  if (!locId) return 'Sem Localização Registada';

  const loc = listaLocalizacoes.value.find(l => l.id_localizacao === locId || l.id === locId);
  if (!loc) return 'Sala Não Encontrada';

  const predioId = loc.predio || loc.id_predio;
  const predio = listaPredios.value.find(p => p.id_predio === predioId || p.id === predioId);

  const nomePredio = predio ? (predio.nome_predio || predio.nome) : 'Prédio N/I';
  const nomeLoc = loc.desc_localizacao || loc.nome || 'Sala N/I';

  return `${nomePredio} - ${nomeLoc}`;
}

const ativosFiltrados = computed(() => {
  if (!termoBusca.value) return ativos.value
  const termo = termoBusca.value.toLowerCase()
  return ativos.value.filter(a => {
    const busca = `${a.codigo_patrimonial} ${a.marca} ${a.modelo} ${a.tipo_ativo}`.toLowerCase()
    return busca.includes(termo)
  })
})

const localizacoesFiltradas = computed(() => {
  if (!idPredioSelecionado.value) return []
  return listaLocalizacoes.value.filter(l => (l.predio === idPredioSelecionado.value) || (l.id_predio === idPredioSelecionado.value))
})

async function carregarDados() {
  loading.value = true
  try {
    const [resAtivos, resPredios, resLoc] = await Promise.all([
      api.get('/ativo/', authHeader()),
      api.get('/predio/', authHeader()),
      api.get('/localizacao/', authHeader())
    ])
    ativos.value = resAtivos.data.dados || resAtivos.data || []
    listaPredios.value = resPredios.data.dados || resPredios.data || []
    listaLocalizacoes.value = resLoc.data.dados || resLoc.data || []
  } catch (error) {
    console.error('Erro ao buscar dados:', error)
  } finally {
    loading.value = false
  }
}

function aoTrocarPredio() {
  form.value.id_localizacao = '' 
}

function resetarForm() {
  form.value = {
    id_ativo: null,
    codigo_patrimonial: '',
    tipo_ativo: 'AR_CONDICIONADO',
    marca: '',
    modelo: '',
    numero_serial: '',
    periodicidade_preventiva_dias: 30,
    id_localizacao: ''
  }
  idPredioSelecionado.value = null
}

function abrirModalNovo() {
  resetarForm()
  modoEdicao.value = false
  modalAberto.value = true
}

function abrirModalEdicao(ativo: any) {
  modoEdicao.value = true

  const idAtivoReal = ativo.id_ativo || ativo.id;
  const locIdReal = ativo.localizacao || ativo.id_localizacao || ativo.localizacao_id;

  form.value = { 
    id_ativo: idAtivoReal, 
    codigo_patrimonial: ativo.codigo_patrimonial || '',
    tipo_ativo: ativo.tipo_ativo || 'AR_CONDICIONADO',
    marca: ativo.marca || '',
    modelo: ativo.modelo || '',
    numero_serial: ativo.numero_serial || '',
    periodicidade_preventiva_dias: ativo.periodicidade_preventiva_dias || 30,
    id_localizacao: locIdReal || ''
  }

  const locEncontrada = listaLocalizacoes.value.find(l => l.id_localizacao === locIdReal || l.id === locIdReal)
  if (locEncontrada) {
    idPredioSelecionado.value = locEncontrada.predio || locEncontrada.id_predio
  }
  
  modalAberto.value = true
}

function fecharModal() {
  modalAberto.value = false
}

async function salvarAtivo() {
  if (!form.value.codigo_patrimonial || !form.value.marca || !form.value.modelo || !form.value.id_localizacao) {
    return Swal.fire({ title: 'Atenção', text: 'Preencha todos os campos obrigatórios (*).', icon: 'warning' })
  }

  salvando.value = true
  try {
    const payload = {
      codigo_patrimonial: form.value.codigo_patrimonial,
      tipo_ativo: form.value.tipo_ativo,
      marca: form.value.marca,
      modelo: form.value.modelo,
      numero_serial: form.value.numero_serial,
      periodicidade_preventiva_dias: form.value.periodicidade_preventiva_dias,
      id_localizacao: form.value.id_localizacao,
      localizacao: form.value.id_localizacao 
    }

    if (modoEdicao.value) {
      if (!form.value.id_ativo) throw new Error("ID do Ativo não foi encontrado no Frontend.");
      await api.put(`/ativo/${form.value.id_ativo}/`, payload, authHeader())
      Swal.fire({ title: 'Atualizado!', text: 'Ativo atualizado com sucesso.', icon: 'success', timer: 2000, showConfirmButton: false })
    } else {
      await api.post('/ativo/', payload, authHeader())
      Swal.fire({ title: 'Criado!', text: 'Novo ativo registado com sucesso.', icon: 'success', timer: 2000, showConfirmButton: false })
    }

    fecharModal()
    await carregarDados()
  } catch (error: any) {
    let msgDetalhada = 'Verifique os dados informados.';

    if (error.response && error.response.data) {
      const resposta = error.response.data;

      if (resposta.erros && typeof resposta.erros === 'object') {
        msgDetalhada = Object.entries(resposta.erros)
          .map(([campo, msgs]) => {
            const textoErro = Array.isArray(msgs) ? msgs.join(', ') : String(msgs);
            return `- ${textoErro}`; 
          })
          .join('\n');
      } 
      else if (resposta.mensagem) {
        msgDetalhada = resposta.mensagem;
      }
    }
    
    Swal.fire({ 
      title: 'Não foi possível salvar', 
      text: msgDetalhada, 
      icon: 'error',
      customClass: { popup: 'rounded-2xl' }
    })
  } finally {
    salvando.value = false
  }
}

async function excluirAtivo(id: number) {
  const result = await Swal.fire({ title: 'Remover Ativo?', text: 'Tem a certeza que deseja remover este equipamento?', icon: 'warning', showCancelButton: true, confirmButtonColor: '#ef4444', confirmButtonText: 'Sim, Remover', cancelButtonText: 'Cancelar' })
  if (!result.isConfirmed) return

  try {
    await api.delete(`/ativo/${id}/`, authHeader())
    Swal.fire({ title: 'Removido!', text: 'Ativo excluído com sucesso.', icon: 'success', timer: 2000, showConfirmButton: false })
    carregarDados()
  } catch (error) {
    Swal.fire({ title: 'Erro', text: 'Não foi possível remover o ativo. Ele pode estar vinculado a uma OS.', icon: 'error' })
  }
}

onMounted(() => carregarDados())
</script>

<style scoped> .animate-fade-in { animation: fadeIn 0.2s ease-out; } @keyframes fadeIn { from { opacity: 0; transform: scale(0.98); } to { opacity: 1; transform: scale(1); } } </style>