<script setup>
import { useRoute } from 'vue-router'
import { useApi } from '../../composables/useApi.js'

const route = useRoute()
const { data: photos, loading, error } = useApi({
  immediate: true,
  parseErrorDetail: true,
  url: () => `/mars-rovers/${route.params.rover}/latest-photos`,
  transform: (data) => data.latest_photos ?? data.photos ?? [],
})
const roverName = {
  curiosity: 'Curiosity',
  perseverance: 'Perseverance',
  opportunity: 'Opportunity',
  spirit: 'Spirit',
}
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <h1 class="text-4xl font-bold mb-1">{{ roverName[route.params.rover] ?? route.params.rover }}</h1>
    </header>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <!-- Erro -->
    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <!-- Vazio -->
    <p v-else-if="photos?.length === 0" class="text-sm text-white/40 py-16">
      Nenhuma foto encontrada para este Sol neste rover.
    </p>

    <!-- Lista -->
    <div v-else class="flex flex-col gap-3">
      <div
        v-for="photo in photos?.slice(0, 30)"
        :key="photo.id"
        class="flex items-stretch gap-0 rounded-xl border border-white/[0.08] bg-white/[0.03] overflow-hidden hover:bg-white/[0.05] transition-colors"
      >
        <!-- Imagem generosa à esquerda -->
        <div class="shrink-0 w-56 h-40">
          <img
            :src="photo.img_src"
            :alt="`${photo.rover?.name} - ${photo.camera?.full_name}`"
            class="w-full h-full object-cover"
            loading="lazy"
          />
        </div>

        <!-- Divisor -->
        <div class="w-px bg-white/[0.06] shrink-0" />

        <!-- Conteúdo -->
        <div class="flex flex-1 items-center gap-8 px-6">

          <!-- Câmera -->
          <div class="flex-1 min-w-0">
            <p class="text-sm font-semibold text-white/85 truncate">{{ photo.camera?.full_name }}</p>
            <p class="text-xs text-white/35 mt-0.5 font-mono">{{ photo.camera?.name }}</p>
          </div>

          <!-- Metadados -->
          <div class="shrink-0 flex items-center gap-6 text-xs">
            <div class="flex flex-col gap-0.5 text-right">
              <span class="text-[10px] uppercase tracking-widest text-white/30">Sol</span>
              <span class="text-white/65 font-mono">{{ photo.sol }}</span>
            </div>
            <div class="w-px h-6 bg-white/[0.08]" />
            <div class="flex flex-col gap-0.5 text-right">
              <span class="text-[10px] uppercase tracking-widest text-white/30">Data</span>
              <span class="text-white/65 font-mono">{{ photo.earth_date }}</span>
            </div>
            <div class="w-px h-6 bg-white/[0.08]" />
            <div class="flex flex-col gap-0.5 text-right">
              <span class="text-[10px] uppercase tracking-widest text-white/30">ID</span>
              <span class="text-white/35 font-mono">#{{ photo.id }}</span>
            </div>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>