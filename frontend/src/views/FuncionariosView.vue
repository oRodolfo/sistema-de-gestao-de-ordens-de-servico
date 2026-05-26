<template>
  <div class="p-8">

    <!-- Cabeçalho -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-xl font-semibold text-gray-800">Funcionários</h1>
        <p class="text-sm text-gray-400 mt-0.5">Gerencie os usuários do sistema</p>
      </div>
      <button @click="mostrarModal = true"
        class="bg-blue-800 text-white text-sm px-4 py-2 rounded font-medium hover:bg-blue-700 cursor-pointer transition-colors">
        + Novo Funcionário
      </button>
    </div>

    <!-- Barra de filtros -->
    <div class="bg-white border border-gray-200 rounded-lg px-4 py-3 mb-4 flex gap-3 items-center">
      <span class="text-xs text-gray-400 font-medium uppercase tracking-wide shrink-0">Filtrar por</span>
      <select v-model="filtroCargo"
        class="text-sm border border-gray-200 rounded px-3 py-1.5 outline-none focus:border-blue-600 cursor-pointer">
        <option value="">Todos os cargos</option>
        <option v-for="g in grupos" :key="g.id_grupo" :value="g.desc_grupo">{{ g.desc_grupo }}</option>
      </select>
      <input v-model="busca" type="text" placeholder="Buscar por nome ou email..."
        class="text-sm border border-gray-200 rounded px-3 py-1.5 outline-none focus:border-blue-600 flex-1" />
      <button v-if="filtroCargo || busca"
        @click="filtroCargo = ''; busca = ''"
        class="text-xs text-gray-400 hover:text-gray-600 cursor-pointer whitespace-nowrap">
        Limpar filtros
      </button>
    </div>

    <!-- Tabela -->
    <div class="bg-white border border-gray-200 rounded-lg overflow-hidden">
      <table class="w-full">
        <thead>
          <tr class="bg-gray-50 border-b border-gray-200">
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide">Nome</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide">Email</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide w-32">Cargo</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide w-24">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-if="funcionariosFiltrados.length === 0">
            <td colspan="4" class="px-4 py-10 text-center text-sm text-gray-400">Nenhum funcionário encontrado.</td>
          </tr>
          <tr v-for="funcionario in funcionariosFiltrados" :key="funcionario.id_usuario"
            class="hover:bg-gray-50 transition-colors">
            <td class="px-4 py-3 text-sm text-gray-800 font-medium">{{ funcionario.nome }}</td>
            <td class="px-4 py-3 text-sm text-gray-500">{{ funcionario.email }}</td>
            <td class="px-4 py-3">
              <span v-if="funcionario.grupo_descricao"
                :class="['px-2 py-0.5 rounded text-xs font-medium', corCargo(funcionario.grupo_descricao)]">
                {{ funcionario.grupo_descricao }}
              </span>
              <span v-else class="text-xs text-gray-300">—</span>
            </td>
            <td class="px-4 py-3 text-sm flex gap-3">
              <button @click="abrirEditar(funcionario)"
                class="text-xs text-blue-700 hover:text-blue-900 font-medium cursor-pointer border border-blue-200 hover:border-blue-400 px-2 py-1 rounded transition-colors">
                Editar
              </button>
              <button @click="confirmarDelete(funcionario)"
                class="text-xs text-red-500 hover:text-red-700 font-medium cursor-pointer border border-red-200 hover:border-red-400 px-2 py-1 rounded transition-colors">
                Deletar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="px-4 py-3 border-t border-gray-100 bg-gray-50">
        <span class="text-xs text-gray-400">Exibindo {{ funcionariosFiltrados.length }} de {{ funcionarios.length }} registros</span>
      </div>
    </div>

    <!-- Modal Novo Funcionário -->
    <div v-if="mostrarModal" @click.self="mostrarModal = false"
      class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
      <div class="bg-white rounded-lg w-full max-w-md shadow-xl border border-gray-200 overflow-hidden">
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100 bg-gray-50">
          <h2 class="text-sm font-semibold text-gray-800">Novo Funcionário</h2>
          <button @click="mostrarModal = false" class="text-gray-400 hover:text-gray-600 cursor-pointer text-lg leading-none">✕</button>
        </div>
        <div class="px-6 py-5 flex flex-col gap-4">
          <div class="flex flex-col gap-1">
            <label class="text-xs text-gray-400 uppercase tracking-wide font-medium">Nome</label>
            <input v-model="novoFuncionario.nome" type="text" placeholder="Nome completo"
              class="text-sm border border-gray-200 rounded px-3 py-2 outline-none focus:border-blue-600" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-xs text-gray-400 uppercase tracking-wide font-medium">Email</label>
            <input v-model="novoFuncionario.email" type="email" placeholder="email@fho.edu.br"
              class="text-sm border border-gray-200 rounded px-3 py-2 outline-none focus:border-blue-600" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-xs text-gray-400 uppercase tracking-wide font-medium">Senha</label>
            <input v-model="novoFuncionario.senha" type="password" placeholder="••••••••"
              class="text-sm border border-gray-200 rounded px-3 py-2 outline-none focus:border-blue-600" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-xs text-gray-400 uppercase tracking-wide font-medium">Cargo</label>
            <select v-model="novoFuncionario.grupo"
              class="text-sm border border-gray-200 rounded px-3 py-2 outline-none focus:border-blue-600 cursor-pointer">
              <option value="">Selecione o cargo</option>
              <option v-for="g in grupos" :key="g.id_grupo" :value="g.id_grupo">{{ g.desc_grupo }}</option>
            </select>
          </div>
        </div>
        <div class="flex gap-2 px-6 py-4 border-t border-gray-100">
          <button @click="mostrarModal = false"
            class="flex-1 py-2 text-sm rounded border border-gray-300 text-gray-600 hover:bg-gray-50 cursor-pointer">Cancelar</button>
          <button @click="mostrarConfirmacaoCadastro = true"
            class="flex-1 py-2 text-sm rounded bg-blue-800 text-white hover:bg-blue-700 cursor-pointer">Salvar</button>
        </div>
      </div>
    </div>

    <!-- Modal Confirmação Cadastro -->
    <div v-if="mostrarConfirmacaoCadastro" @click.self="mostrarConfirmacaoCadastro = false"
      class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
      <div class="bg-white rounded-lg w-full max-w-sm shadow-xl border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 bg-gray-50">
          <h2 class="text-sm font-semibold text-gray-800">Confirmar cadastro</h2>
        </div>
        <div class="px-6 py-5">
          <p class="text-sm text-gray-500">Deseja cadastrar <span class="font-medium text-gray-800">{{ novoFuncionario.nome }}</span>?</p>
        </div>
        <div class="flex gap-2 px-6 py-4 border-t border-gray-100">
          <button @click="mostrarConfirmacaoCadastro = false"
            class="flex-1 py-2 text-sm rounded border border-gray-300 text-gray-600 hover:bg-gray-50 cursor-pointer">Cancelar</button>
          <button @click="salvarFuncionario"
            class="flex-1 py-2 text-sm rounded bg-blue-800 text-white hover:bg-blue-700 cursor-pointer">Confirmar</button>
        </div>
      </div>
    </div>

    <!-- Modal Deletar -->
    <div v-if="mostrarModalDeletar" @click.self="mostrarModalDeletar = false"
      class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
      <div class="bg-white rounded-lg w-full max-w-sm shadow-xl border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 bg-gray-50">
          <h2 class="text-sm font-semibold text-gray-800">Confirmar exclusão</h2>
        </div>
        <div class="px-6 py-5">
          <p class="text-sm text-gray-500">Deseja remover <span class="font-medium text-gray-800">{{ funcionarioParaDeletar?.nome }}</span>? Esta ação não pode ser desfeita.</p>
        </div>
        <div class="flex gap-2 px-6 py-4 border-t border-gray-100">
          <button @click="mostrarModalDeletar = false"
            class="flex-1 py-2 text-sm rounded border border-gray-300 text-gray-600 hover:bg-gray-50 cursor-pointer">Cancelar</button>
          <button @click="deletarFuncionario"
            class="flex-1 py-2 text-sm rounded bg-red-500 text-white hover:bg-red-600 cursor-pointer">Remover</button>
        </div>
      </div>
    </div>

    <!-- Modal Editar -->
    <div v-if="mostrarModalEditar" @click.self="mostrarModalEditar = false"
      class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
      <div class="bg-white rounded-lg w-full max-w-md shadow-xl border border-gray-200 overflow-hidden">
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100 bg-gray-50">
          <h2 class="text-sm font-semibold text-gray-800">Editar Funcionário</h2>
          <button @click="mostrarModalEditar = false" class="text-gray-400 hover:text-gray-600 cursor-pointer text-lg leading-none">✕</button>
        </div>
        <div class="px-6 py-5 flex flex-col gap-4">
          <div class="flex flex-col gap-1">
            <label class="text-xs text-gray-400 uppercase tracking-wide font-medium">Nome</label>
            <input v-model="funcionarioEditando.nome" type="text"
              class="text-sm border border-gray-200 rounded px-3 py-2 outline-none focus:border-blue-600" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-xs text-gray-400 uppercase tracking-wide font-medium">Email</label>
            <input v-model="funcionarioEditando.email" type="email"
              class="text-sm border border-gray-200 rounded px-3 py-2 outline-none focus:border-blue-600" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-xs text-gray-400 uppercase tracking-wide font-medium">Cargo</label>
            <select v-model="funcionarioEditando.grupo"
              class="text-sm border border-gray-200 rounded px-3 py-2 outline-none focus:border-blue-600 cursor-pointer">
              <option value="">Selecione o cargo</option>
              <option v-for="g in grupos" :key="g.id_grupo" :value="g.id_grupo">{{ g.desc_grupo }}</option>
            </select>
          </div>
        </div>
        <div class="flex gap-2 px-6 py-4 border-t border-gray-100">
          <button @click="mostrarModalEditar = false"
            class="flex-1 py-2 text-sm rounded border border-gray-300 text-gray-600 hover:bg-gray-50 cursor-pointer">Cancelar</button>
          <button @click="mostrarConfirmacaoEdicao = true"
            class="flex-1 py-2 text-sm rounded bg-blue-800 text-white hover:bg-blue-700 cursor-pointer">Salvar</button>
        </div>

        <!-- Modal Confirmação Edição (dentro do editar) -->
        <div v-if="mostrarConfirmacaoEdicao" @click.self="mostrarConfirmacaoEdicao = false"
          class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
          <div class="bg-white rounded-lg w-full max-w-sm shadow-xl border border-gray-200 overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-100 bg-gray-50">
              <h2 class="text-sm font-semibold text-gray-800">Confirmar alteração</h2>
            </div>
            <div class="px-6 py-5">
              <p class="text-sm text-gray-500">Deseja salvar as alterações de <span class="font-medium text-gray-800">{{ funcionarioEditando?.nome }}</span>?</p>
            </div>
            <div class="flex gap-2 px-6 py-4 border-t border-gray-100">
              <button @click="mostrarConfirmacaoEdicao = false"
                class="flex-1 py-2 text-sm rounded border border-gray-300 text-gray-600 hover:bg-gray-50 cursor-pointer">Cancelar</button>
              <button @click="salvarEdicao"
                class="flex-1 py-2 text-sm rounded bg-blue-800 text-white hover:bg-blue-700 cursor-pointer">Confirmar</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Sucesso -->
    <div v-if="mostrarModalSucesso" @click.self="mostrarModalSucesso = false"
      class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
      <div class="bg-white rounded-lg w-full max-w-sm shadow-xl border border-gray-200 overflow-hidden">
        <div class="px-6 py-8 text-center flex flex-col items-center">
          <div class="w-12 h-12 bg-green-50 border border-green-200 rounded-full flex items-center justify-center text-green-600 text-xl mb-4">✓</div>
          <h2 class="text-base font-semibold text-gray-800 mb-1">{{ tituloSucesso }}</h2>
          <p class="text-sm text-gray-400 mb-6">{{ mensagemSucesso }}</p>
          <button @click="mostrarModalSucesso = false"
            class="w-full py-2 text-sm rounded bg-blue-800 text-white hover:bg-blue-700 cursor-pointer">Fechar</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'

const funcionarios = ref([])
const grupos = ref<any[]>([])
const busca = ref('')
const filtroCargo = ref('')
const mostrarModal = ref(false)
const novoFuncionario = ref({ nome: '', email: '', senha: '', grupo: '' })
const mostrarConfirmacaoCadastro = ref(false)
const mostrarModalDeletar = ref(false)
const funcionarioParaDeletar = ref<any>(null)
const mostrarModalEditar = ref(false)
const funcionarioEditando = ref<any>(null)
const mostrarConfirmacaoEdicao = ref(false)
const mostrarModalSucesso = ref(false)
const tituloSucesso = ref('')
const mensagemSucesso = ref('')

onMounted(async () => {
  const [resUsuarios, resGrupos] = await Promise.all([
    api.get('/usuario/'),
    api.get('/grupo/')
  ])
  funcionarios.value = resUsuarios.data
  grupos.value = resGrupos.data
})

const funcionariosFiltrados = computed(() => {
  return funcionarios.value.filter((f: any) => {
    const buscaOk = !busca.value ||
      f.nome?.toLowerCase().includes(busca.value.toLowerCase()) ||
      f.email?.toLowerCase().includes(busca.value.toLowerCase())
    const cargoOk = !filtroCargo.value || f.grupo_descricao === filtroCargo.value
    return buscaOk && cargoOk
  })
})

function corCargo(cargo: string) {
  const cores: Record<string, string> = {
    GERENTE: 'bg-blue-50 text-blue-700',
    GESTOR: 'bg-purple-50 text-purple-700',
    TECNICO: 'bg-yellow-50 text-yellow-700',
    SOLICITANTE: 'bg-gray-100 text-gray-600',
  }
  return cores[cargo] || 'bg-gray-100 text-gray-500'
}

function dispararSucesso(titulo: string, mensagem: string) {
  tituloSucesso.value = titulo
  mensagemSucesso.value = mensagem
  mostrarModalSucesso.value = true
}

async function salvarFuncionario() {
  try {
    await api.post('/usuario/', {
      nome: novoFuncionario.value.nome,
      email: novoFuncionario.value.email,
      senha: novoFuncionario.value.senha,
      grupo: novoFuncionario.value.grupo
    })
    const res = await api.get('/usuario/')
    funcionarios.value = res.data
    mostrarModal.value = false
    mostrarConfirmacaoCadastro.value = false
    novoFuncionario.value = { nome: '', email: '', senha: '', grupo: '' }
    dispararSucesso('Cadastrado!', 'O novo funcionário foi adicionado com sucesso.')
  } catch (e) {
    console.error('Erro ao salvar funcionário', e)
  }
}

function confirmarDelete(funcionario: any) {
  funcionarioParaDeletar.value = funcionario
  mostrarModalDeletar.value = true
}

async function deletarFuncionario() {
  try {
    await api.delete(`/usuario/${funcionarioParaDeletar.value.id_usuario}/`)
    funcionarios.value = funcionarios.value.filter(
      (f: any) => f.id_usuario !== funcionarioParaDeletar.value.id_usuario
    )
    mostrarModalDeletar.value = false
    funcionarioParaDeletar.value = null
    dispararSucesso('Excluído!', 'O funcionário foi removido do sistema com sucesso.')
  } catch (e) {
    console.error('Erro ao deletar', e)
  }
}

function abrirEditar(funcionario: any) {
  funcionarioEditando.value = {
    ...funcionario,
    grupo: funcionario.id_grupo ? Number(funcionario.id_grupo) : ''
  }
  mostrarModalEditar.value = true
}

async function salvarEdicao() {
  try {
    await api.patch(`/usuario/${funcionarioEditando.value.id_usuario}/`, {
      nome: funcionarioEditando.value.nome,
      email: funcionarioEditando.value.email,
      grupo: Number(funcionarioEditando.value.grupo)
    })
    const res = await api.get('/usuario/')
    funcionarios.value = res.data
    mostrarModalEditar.value = false
    mostrarConfirmacaoEdicao.value = false
    funcionarioEditando.value = null
    dispararSucesso('Atualizado!', 'As alterações foram salvas com sucesso.')
  } catch (e) {
    console.error('Erro ao editar', e)
  }
}
</script>