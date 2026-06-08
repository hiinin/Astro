<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const photos = ref(null)
const loading = ref(true)
const error = ref(null)

const roverName = {
  curiosity: 'Curiosity',
  perseverance: 'Perseverance',
  opportunity: 'Opportunity',
  spirit: 'Spirit',
}

onMounted(async () => {
  try {
    const res = await fetch(`/api/mars-rovers/${route.params.rover}/photos?sol=1000`)
    if (!res.ok) throw new Error(res.status)
    const data = await res.json()
    photos.value = data.photos ?? []
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <nav class="mb-3 text-xs text-white/40">
        <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
        <span> › </span>
        <router-link to="/rovers-marte" class="hover:text-white/70 transition-colors">Rovers em Marte</router-link>
        <span> › {{ roverName[route.params.rover] ?? route.params.rover }}</span>
      </nav>
      <h1 class="text-2xl font-bold mb-1">{{ roverName[route.params.rover] ?? route.params.rover }}</h1>
      <p class="text-sm text-white/40">Fotos do Sol marciano 1000. Dados via NASA Mars Rover Photos API.</p>
    </header>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <p v-else-if="photos?.length === 0" class="text-sm text-white/40 py-16">
      Nenhuma foto encontrada para este Sol neste rover.
    </p>

    <div v-else class="grid grid-cols-3 gap-4">
      <div
        v-for="photo in photos?.slice(0, 30)"
        :key="photo.id"
        class="rounded-xl border border-white/[0.08] bg-white/[0.03] overflow-hidden"
      >
        <img
          :src="photo.img_src"
          :alt="`${photo.rover?.name} - ${photo.camera?.full_name}`"
          class="w-full aspect-square object-cover"
          loading="lazy"
        />
        <div class="p-3">
          <p class="text-xs font-medium text-white/80 truncate">{{ photo.camera?.full_name }}</p>
          <p class="text-[11px] text-white/40 mt-0.5">Sol {{ photo.sol }} · {{ photo.earth_date }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
