<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRequest as useApi } from '../../composables'
import { mediaThumb } from '../../composables'

const router = useRouter()
const query = ref('Earth')
const { data: results, loading, error, searched, search } = useApi()

function handleSearch() {
  if (!query.value.trim()) return
  search(`/images/search?q=${encodeURIComponent(query.value)}&media_type=image`, {
    transform: (data) => data.collection?.items ?? [],
  })
}

onMounted(() => {
  handleSearch()
})

function openMedia(item) {
  const d = item.data?.[0]
  if (d?.nasa_id) router.push({ path: `/midias/${d.nasa_id}`, query: { title: d.title } })
}
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">

    <!-- Header -->
    <header class="mb-10">
      <h1 class="text-3xl font-bold tracking-tight mb-2">Mídias</h1>
    </header>

    <!-- Search bar -->
    <form @submit.prevent="handleSearch" class="flex gap-3 mb-10 w-full">
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

    <!-- Loading state -->
    <div v-if="loading" class="flex flex-col items-center gap-3 text-sm text-white/40 py-20">
      <span class="size-6 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      <span>Buscando mídias...</span>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="text-center py-20">
      <p class="text-sm text-red-400/80 bg-red-500/[0.06] border border-red-500/20 inline-block px-5 py-3 rounded-lg">
        Falha ao carregar os dados ({{ error }}).
      </p>
    </div>

    <!-- Empty state -->
    <div v-else-if="searched && results?.length === 0" class="text-center py-20">
      <p class="text-white/40 text-sm">Nenhuma mídia encontrada para "<span class="text-white/60">{{ query }}</span>".</p>
    </div>

    <!-- Results grid -->
    <div v-else-if="results?.length">
      <p class="text-xs text-white/30 mb-4">Exibindo {{ Math.min(results.length, 30) }} resultados</p>

      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
        <div
          v-for="(item, i) in results.slice(0, 30)"
          :key="i"
          class="group rounded-2xl border border-white/[0.07] bg-white/[0.02] overflow-hidden hover:border-white/[0.15] hover:bg-white/[0.04] transition-all duration-300 hover:-translate-y-0.5 hover:shadow-xl hover:shadow-black/30 cursor-pointer"
          @click="openMedia(item)"
        >
          <div class="aspect-[4/3] bg-white/[0.03] flex items-center justify-center overflow-hidden relative">
            <img
              v-if="mediaThumb(item)"
              :src="mediaThumb(item)"
              :alt="item.data?.[0]?.title"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              loading="lazy"
            />
            <span v-else class="text-white/20 text-xs">Sem prévia</span>
            <!-- Overlay gradient on hover -->
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          </div>
          <div class="p-4">
            <p class="text-xs font-medium text-white/80 line-clamp-2 leading-snug mb-2">{{ item.data?.[0]?.title }}</p>
            <div class="flex items-center justify-between">
              <span class="text-[10px] text-white/30">{{ item.data?.[0]?.date_created?.split('T')[0] }}</span>
              <span class="text-[10px] text-white/30">Ver detalhe →</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Initial empty state -->
    <div v-else-if="!searched" class="flex flex-col items-center justify-center py-24 gap-4">
      <div class="size-16 rounded-full bg-white/[0.03] border border-white/[0.08] flex items-center justify-center">
        <svg class="size-7 text-white/20" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909M3.75 21h16.5A2.25 2.25 0 0 0 22.5 18.75V5.25A2.25 2.25 0 0 0 20.25 3H3.75A2.25 2.25 0 0 0 1.5 5.25v13.5A2.25 2.25 0 0 0 3.75 21Z" />
        </svg>
      </div>
      <p class="text-white/30 text-sm">Pesquise na biblioteca de imagens da NASA</p>
    </div>
  </div>
</template>
