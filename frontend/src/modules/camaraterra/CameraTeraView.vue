<script setup>
import { useApi } from '../../composables/useApi.js'

function epicImageUrl(img) {
  const [y, m, d] = img.date.split(' ')[0].split('-')
  return `https://epic.gsfc.nasa.gov/archive/natural/${y}/${m}/${d}/png/${img.image}.png`
}

const { data: images, loading, error } = useApi({ immediate: true, url: '/epic/natural' })
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <nav class="mb-3 text-xs text-white/40">
        <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
        <span> › Câmera da Terra</span>
      </nav>
      <h1 class="text-2xl font-bold mb-1">Câmera da Terra</h1>
      <p class="text-sm text-white/40">Imagens naturais da Terra capturadas pela câmera DSCOVR/EPIC.</p>
    </header>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <div v-else-if="images" class="grid grid-cols-4 gap-4">
      <div
        v-for="img in images.slice(0, 16)"
        :key="img.identifier"
        class="rounded-xl border border-white/[0.08] bg-white/[0.03] overflow-hidden"
      >
        <img
          :src="epicImageUrl(img)"
          :alt="img.caption"
          class="w-full aspect-square object-cover"
          loading="lazy"
        />
        <div class="p-3">
          <p class="text-[11px] text-white/50">{{ img.date?.split(' ')[0] }}</p>
          <p class="text-xs text-white/70 mt-1 truncate">{{ img.caption }}</p>
          <dl class="mt-2 grid grid-cols-2 gap-x-3 gap-y-1 text-[10px] text-white/35">
            <div>
              <span class="text-white/20">Lat </span>{{ img.centroid_coordinates?.lat?.toFixed(2) }}°
            </div>
            <div>
              <span class="text-white/20">Lon </span>{{ img.centroid_coordinates?.lon?.toFixed(2) }}°
            </div>
          </dl>
        </div>
      </div>
    </div>
  </div>
</template>
