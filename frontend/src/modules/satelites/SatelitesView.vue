<script setup>
import { ref } from 'vue'

const query = ref('')
const results = ref(null)
const loading = ref(false)
const error = ref(null)
const searched = ref(false)

async function search() {
  if (!query.value.trim()) return
  loading.value = true
  error.value = null
  results.value = null
  searched.value = true
  try {
    const res = await fetch(`/api/tle?search=${encodeURIComponent(query.value)}`)
    if (!res.ok) throw new Error(res.status)
    const data = await res.json()
    results.value = data.member ?? data ?? []
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <nav class="mb-3 text-xs text-white/40">
        <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
        <span> › Satélites</span>
      </nav>
      <h1 class="text-2xl font-bold mb-1">Satélites</h1>
      <p class="text-sm text-white/40">Elementos orbitais TLE de satélites via CelesTrak.</p>
    </header>

    <form @submit.prevent="search" class="flex gap-3 mb-6">
      <input
        v-model="query"
        placeholder="Ex: ISS, Hubble, Starlink..."
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
      Nenhum satélite encontrado para "{{ query }}".
    </p>

    <div v-else-if="results?.length" class="rounded-xl border border-white/[0.08] overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-white/[0.08] text-left text-xs text-white/40 uppercase tracking-wider">
            <th class="px-5 py-3 font-medium">Nome</th>
            <th class="px-5 py-3 font-medium">ID (NORAD)</th>
            <th class="px-5 py-3 font-medium">Época</th>
            <th class="px-5 py-3 font-medium">Inclinação</th>
            <th class="px-5 py-3 font-medium">Tipo de Órbita</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="sat in results.slice(0, 50)"
            :key="sat['@id']"
            class="border-b border-white/[0.05] last:border-0 hover:bg-white/[0.02]"
          >
            <td class="px-5 py-3.5 font-medium">{{ sat.name }}</td>
            <td class="px-5 py-3.5 text-white/50 font-mono text-xs">{{ sat.satelliteId }}</td>
            <td class="px-5 py-3.5 text-white/50 text-xs">{{ sat.date?.split('T')[0] ?? '—' }}</td>
            <td class="px-5 py-3.5 text-white/60">{{ sat.inclination != null ? `${Number(sat.inclination).toFixed(2)}°` : '—' }}</td>
            <td class="px-5 py-3.5 text-white/50 text-xs">{{ sat.type ?? '—' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else-if="!searched" class="text-center py-16">
      <p class="text-white/30 text-sm">Digite o nome de um satélite para buscar.</p>
    </div>
  </div>
</template>
