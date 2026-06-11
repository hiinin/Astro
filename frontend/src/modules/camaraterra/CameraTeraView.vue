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
      <h1 class="text-4xl font-bold mb-1">Câmera da Terra</h1>
      <p class="text-sm text-white/40">Imagens naturais da Terra capturadas pela câmera DSCOVR/EPIC.</p>
    </header>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <div v-else-if="images" class="rounded-2xl border border-white/[0.08] overflow-hidden">
      <table class="w-full text-xs">
        <thead>
          <tr class="bg-white/[0.04] border-b border-white/[0.08] text-white/40 uppercase tracking-widest text-[10px] font-medium">
            <th class="px-5 py-3 text-left w-14">Foto</th>
            <th class="px-5 py-3 text-left">Imagem</th>
            <th class="px-5 py-3 text-left">Data</th>
            <th class="px-5 py-3 text-left">Legenda</th>
            <th class="px-5 py-3 text-right">Lat</th>
            <th class="px-5 py-3 text-right">Lon</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="img in images.slice(0, 16)"
            :key="img.identifier"
            class="border-b border-white/[0.04] last:border-0 hover:bg-white/[0.03] transition-colors"
          >
            <td class="px-4 py-2.5">
              <img
                :src="epicImageUrl(img)"
                :alt="img.caption"
                loading="lazy"
                class="w-10 h-10 rounded-lg object-cover border border-white/[0.08]"
              />
            </td>
            <td class="px-5 py-2.5 font-mono text-white/40 text-[11px]">{{ img.image }}</td>
            <td class="px-5 py-2.5 text-white/60 whitespace-nowrap">{{ img.date?.split(' ')[0] }}</td>
            <td class="px-5 py-2.5 text-white/70 max-w-xs truncate">{{ img.caption }}</td>
            <td class="px-5 py-2.5 text-right font-mono text-white/50">{{ img.centroid_coordinates?.lat?.toFixed(2) }}°</td>
            <td class="px-5 py-2.5 text-right font-mono text-white/50">{{ img.centroid_coordinates?.lon?.toFixed(2) }}°</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>