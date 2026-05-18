<template>
  <div class="p-8">

    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Funcionários</h1>
      <button class="bg-blue-800 text-white px-4 py-2 rounded-lg font-semibold hover:bg-blue-600 cursor-pointer"
        @click="mostrarModal = true">
        + Novo Funcionário
      </button>
    </div>

    <div class="bg-white rounded-lg shadow-sm overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Nome</th>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Email</th>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Cargo</th>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="funcionario in funcionarios" :key="funcionario.id_usuario" class="hover:bg-gray-50">
            <td class="px-6 py-4 text-sm text-gray-800">{{ funcionario.nome }}</td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ funcionario.email }}</td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ funcionario.grupo_descricao || '—' }}</td>
            <td class="px-6 py-4 text-sm flex gap-2">
              <button @click="abrirEditar(funcionario)" class="text-blue-600 hover:text-blue-800 cursor-pointer">Editar</button>
              <button @click="confirmarDelete(funcionario)" class="text-red-500 hover:text-red-700 cursor-pointer">Deletar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="mostrarModal" @click.self="mostrarModal = false"
      class="fixed inset-0 bg-black/65 z-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-8 w-full max-w-md">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-bold text-gray-800">Novo Funcionário</h2>
          <button @click="mostrarModal = false" class="text-gray-400 hover:text-gray-600 cursor-pointer text-xl">✕</button>
        </div>
        <div class="flex flex-col gap-4">
          <div class="flex flex-col gap-1">
            <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Nome</label>
            <input v-model="novoFuncionario.nome" type="text" placeholder="Nome completo"
              class="border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-blue-600" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Email</label>
            <input v-model="novoFuncionario.email" type="email" placeholder="email@fho.edu.br"
              class="border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-blue-600" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Senha</label>
            <input v-model="novoFuncionario.senha" type="password" placeholder="••••••••"
              class="border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-blue-600" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Cargo</label>
            <select v-model="novoFuncionario.grupo"
              class="border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-blue-600 cursor-pointer">
              <option value="">Selecione o cargo</option>
              <option v-for="g in grupos" :key="g.id_grupo" :value="g.id_grupo">{{ g.desc_grupo }}</option>
            </select>
          </div>
          <div class="flex gap-3 mt-2">
            <button @click="mostrarModal = false"
              class="flex-1 py-3 rounded-lg border border-gray-300 text-gray-600 font-semibold hover:bg-gray-50 cursor-pointer">Cancelar</button>
            <button @click="mostrarConfirmacaoCadastro = true"
              class="flex-1 py-3 rounded-lg bg-blue-800 text-white font-semibold hover:bg-blue-600 cursor-pointer">Salvar</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="mostrarConfirmacaoCadastro" @click.self="mostrarConfirmacaoCadastro = false"
      class="fixed inset-0 bg-black/30 z-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-8 w-full max-w-sm">
        <h2 class="text-xl font-bold text-gray-800 mb-2">Confirmar cadastro</h2>
        <p class="text-gray-500 text-sm mb-6">Tem certeza que deseja cadastrar
          <span class="font-semibold text-gray-800">{{ novoFuncionario.nome }}</span>?
        </p>
        <div class="flex gap-3">
          <button @click="mostrarConfirmacaoCadastro = false"
            class="flex-1 py-3 rounded-lg border border-gray-300 text-gray-600 font-semibold hover:bg-gray-50 cursor-pointer">Cancelar</button>
          <button @click="salvarFuncionario"
            class="flex-1 py-3 rounded-lg bg-blue-800 text-white font-semibold hover:bg-blue-600 cursor-pointer">Confirmar</button>
        </div>
      </div>
    </div>

    <div v-if="mostrarModalDeletar" @click.self="mostrarModalDeletar = false"
      class="fixed inset-0 bg-black/30 z-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-8 w-full max-w-sm">
        <h2 class="text-xl font-bold text-gray-800 mb-2">Confirmar exclusão</h2>
        <p class="text-gray-500 text-sm mb-6">Tem certeza que deseja deletar
          <span class="font-semibold text-gray-800">{{ funcionarioParaDeletar?.nome }}</span>?
          Essa ação não pode ser desfeita.
        </p>
        <div class="flex gap-3">
          <button @click="mostrarModalDeletar = false"
            class="flex-1 py-3 rounded-lg border border-gray-300 text-gray-600 font-semibold hover:bg-gray-50 cursor-pointer">Cancelar</button>
          <button @click="deletarFuncionario"
            class="flex-1 py-3 rounded-lg bg-red-500 text-white font-semibold hover:bg-red-600 cursor-pointer">Deletar</button>
        </div>
      </div>
    </div>

    <div v-if="mostrarModalEditar" @click.self="mostrarModalEditar = false"
      class="fixed inset-0 bg-black/30 z-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-8 w-full max-w-md">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-bold text-gray-800">Editar Funcionário</h2>
          <button @click="mostrarModalEditar = false" class="text-gray-400 hover:text-gray-600 cursor-pointer text-xl">✕</button>
        </div>
        <div class="flex flex-col gap-4">
          <div class="flex flex-col gap-1">
            <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Nome</label>
            <input v-model="funcionarioEditando.nome" type="text"
              class="border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-blue-600" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Email</label>
            <input v-model="funcionarioEditando.email" type="email"
              class="border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-blue-600" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Cargo</label>
            <select v-model="funcionarioEditando.grupo"
              class="border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-blue-600 cursor-pointer">
              <option value="">Selecione o cargo</option>
              <option v-for="g in grupos" :key="g.id_grupo" :value="g.id_grupo">{{ g.desc_grupo }}</option>
            </select>
          </div>
          <div class="flex gap-3 mt-2">
            <button @click="mostrarModalEditar = false"
              class="flex-1 py-3 rounded-lg border border-gray-300 text-gray-600 font-semibold hover:bg-gray-50 cursor-pointer">Cancelar</button>
            <button @click="mostrarConfirmacaoEdicao = true"
              class="flex-1 py-3 rounded-lg bg-blue-800 text-white font-semibold hover:bg-blue-600 cursor-pointer">Salvar</button>
          </div>
        </div>

        <div v-if="mostrarConfirmacaoEdicao" @click.self="mostrarConfirmacaoEdicao = false"
          class="fixed inset-0 bg-black/30 z-50 flex items-center justify-center">
          <div class="bg-white rounded-lg p-8 w-full max-w-sm">
            <h2 class="text-xl font-bold text-gray-800 mb-2">Confirmar alteração</h2>
            <p class="text-gray-500 text-sm mb-6">Tem certeza que deseja salvar as alterações de
              <span class="font-semibold text-gray-800">{{ funcionarioEditando?.nome }}</span>?
            </p>
            <div class="flex gap-3">
              <button @click="mostrarConfirmacaoEdicao = false"
                class="flex-1 py-3 rounded-lg border border-gray-300 text-gray-600 font-semibold hover:bg-gray-50 cursor-pointer">Cancelar</button>
              <button @click="salvarEdicao"
                class="flex-1 py-3 rounded-lg bg-blue-800 text-white font-semibold hover:bg-blue-600 cursor-pointer">Confirmar</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="mostrarModalSucesso" @click.self="mostrarModalSucesso = false"
      class="fixed inset-0 bg-black/30 z-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-8 w-full max-w-sm text-center flex flex-col items-center">
        <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center text-green-600 text-3xl mb-4">
          ✓
        </div>
        <h2 class="text-xl font-bold text-gray-800 mb-2">{{ tituloSucesso }}</h2>
        <p class="text-gray-500 text-sm mb-6">{{ mensagemSucesso }}</p>
        <button @click="mostrarModalSucesso = false"
          class="w-full py-3 rounded-lg bg-blue-800 text-white font-semibold hover:bg-blue-600 cursor-pointer">
          Fechar
        </button>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const funcionarios = ref([])
const grupos = ref<any[]>([])
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
    
    dispararSucesso('Atualizado!', 'As alterações do funcionário foram salvas com sucesso.')
  } catch (e) {
    console.error('Erro ao editar', e)
  }
}
</script>