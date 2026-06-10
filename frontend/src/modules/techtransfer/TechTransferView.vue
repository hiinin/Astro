<script setup>
import { ref } from 'vue'
import { useApi } from '../../composables/useApi.js'

const kind = ref('patent')
const query = ref('')
const { data: results, loading, error, searched, search } = useApi()

const kinds = [
  { id: 'patent', label: 'Patentes', param: 'patent' },
  { id: 'software', label: 'Software', param: 'software' },
  { id: 'spinoff', label: 'Spinoffs', param: 'spinoff' },
]

function handleSearch() {
  const q = query.value.trim()
  if (!q) return
  const item = kinds.find((k) => k.id === kind.value) ?? kinds[0]
  search(`/techtransfer/${kind.value}?${item.param}=${encodeURIComponent(q)}`, {
    transform: (data) => data.results ?? [],
  })
}

function title(row) {
  return row?.[1] ?? '—'
}

function link(row) {
  return row?.find((cell) => typeof cell === 'string' && cell.startsWith('http')) ?? null
}
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <nav class="mb-3 text-xs text-white/40">
        <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
        <span> › TechTransfer</span>
      </nav>
      <h1 class="text-2xl font-bold mb-1">TechTransfer</h1>
      <p class="text-sm text-white/40">Patentes, software e spinoffs da NASA.</p>
    </header>

    <div class="flex gap-2 mb-4">
      <button
        v-for="item in kinds"
        :key="item.id"
        type="button"
        class="px-4 py-2 text-sm rounded-lg border transition-colors"
        :class="kind === item.id
          ? 'bg-blue-500/20 border-blue-500/30 text-blue-300'
          : 'border-white/[0.08] text-white/50 hover:text-white/80 hover:bg-white/[0.03]'"
        @click="kind = item.id"
      >
        {{ item.label }}
      </button>
    </div>

    <form @submit.prevent="handleSearch" class="flex gap-3 mb-6">
      <input
        v-model="query"
        placeholder="Buscar..."
        class="flex-1 bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm text-white placeholder-white/30 outline-none focus:border-white/20 transition-colors"
      />
      <button
        type="submit"
        class="px-5 py-2.5 bg-blue-500/20 border border-blue-500/30 text-blue-300 text-sm rounded-lg hover:bg-blue-500/30 transition-colors"
      >
        Buscar
      </button>
    </form>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <p v-else-if="searched && results?.length === 0" class="text-sm text-white/40 py-8">
      Nenhum resultado para "{{ query }}".
    </p>

    <div v-else-if="results?.length" class="rounded-xl border border-white/[0.08] overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-white/[0.08] text-left text-xs text-white/40 uppercase tracking-wider">
            <th class="px-5 py-3 font-medium">Título</th>
            <th class="px-5 py-3 font-medium">Link</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, i) in results"
            :key="i"
            class="border-b border-white/[0.05] last:border-0 hover:bg-white/[0.03]"
          >
            <td class="px-5 py-3.5 font-medium">{{ title(row) }}</td>
            <td class="px-5 py-3.5">
              <a
                v-if="link(row)"
                :href="link(row)"
                target="_blank"
                class="text-xs text-blue-400 hover:underline"
              >
                Ver na NASA ↗
              </a>
              <span v-else class="text-white/25 text-xs">—</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-else class="text-sm text-white/30 py-16 text-center">
      Pesquise patentes, software ou spinoffs da NASA.
    </p>
  </div>
</template>
