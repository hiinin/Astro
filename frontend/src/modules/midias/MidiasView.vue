<script setup>
import { ref } from 'vue'

const query = ref('')
const results = ref(null)
const loading = ref(false)
const error = ref(null)
const searched = ref(false)

function thumbOf(item) {
  const links = item.links ?? []
  const thumb = links.find(l => l.rel === 'preview' || l.href?.endsWith('.jpg') || l.href?.endsWith('.png'))
  return thumb?.href ?? null
}

async function search() {
  if (!query.value.trim()) return
  loading.value = true
  error.value = null
  results.value = null
  searched.value = true
  try {
    const res = await fetch(`/api/images/search?q=${encodeURIComponent(query.value)}&media_type=image`)
    if (!res.ok) throw new Error(res.status)
    const data = await res.json()
    results.value = data.collection?.items ?? []
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
        <span> › Mídias</span>
      </nav>
      <h1 class="text-2xl font-bold mb-1">Mídias</h1>
      <p class="text-sm text-white/40">Biblioteca de imagens e vídeos da NASA.</p>
    </header>

    <form @submit.prevent="search" class="flex gap-3 mb-6">
      <input
        v-model="query"
        placeholder="Ex: Apollo 11, Mars, Hubble..."
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
      Nenhuma mídia encontrada para "{{ query }}".
    </p>

    <div v-else-if="results?.length" class="grid grid-cols-3 gap-4">
      <div
        v-for="(item, i) in results.slice(0, 30)"
        :key="i"
        class="rounded-xl border border-white/[0.08] bg-white/[0.03] overflow-hidden"
      >
        <div class="aspect-video bg-white/[0.03] flex items-center justify-center overflow-hidden">
          <img
            v-if="thumbOf(item)"
            :src="thumbOf(item)"
            :alt="item.data?.[0]?.title"
            class="w-full h-full object-cover"
            loading="lazy"
          />
          <span v-else class="text-white/20 text-xs">Sem prévia</span>
        </div>
        <div class="p-3">
          <p class="text-xs font-medium text-white/80 line-clamp-2 leading-snug">{{ item.data?.[0]?.title }}</p>
          <p class="text-[10px] text-white/35 mt-1">{{ item.data?.[0]?.date_created?.split('T')[0] }}</p>
          <a
            v-if="item.href"
            :href="item.href"
            target="_blank"
            class="text-[10px] text-blue-400 hover:underline mt-1.5 block"
          >
            Ver detalhes ↗
          </a>
        </div>
      </div>
    </div>

    <div v-else-if="!searched" class="text-center py-16">
      <p class="text-white/30 text-sm">Pesquise na biblioteca de imagens da NASA.</p>
    </div>
  </div>
</template>
