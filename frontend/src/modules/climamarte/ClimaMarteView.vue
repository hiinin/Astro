<script setup>
import { computed } from 'vue'
import { useApi } from '../../composables/useApi.js'

const { data: weather, loading, error } = useApi({ immediate: true, url: '/insight/weather' })

const latestSol = computed(() => {
  if (!weather.value?.sol_keys?.length) return null
  const key = weather.value.sol_keys.at(-1)
  return { key, data: weather.value[key] }
})
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <nav class="mb-3 text-xs text-white/40">
        <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
        <span> › Clima em Marte</span>
      </nav>
      <h1 class="text-2xl font-bold mb-1">Clima em Marte</h1>
      <p class="text-sm text-white/40">Dados meteorológicos da missão InSight na superfície marciana.</p>
    </header>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <template v-else-if="latestSol">
      <p class="text-xs text-white/35 mb-5">
        Sol marciano {{ latestSol.key }} · {{ latestSol.data.Season ?? '—' }}
      </p>

      <div class="grid grid-cols-4 gap-4 mb-6">
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-2">Temperatura média</p>
          <p class="text-2xl font-bold">{{ latestSol.data.AT?.av ?? '—' }}°C</p>
          <p class="text-xs text-white/40 mt-1">
            min {{ latestSol.data.AT?.mn }} · max {{ latestSol.data.AT?.mx }}
          </p>
        </div>
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-2">Vento</p>
          <p class="text-2xl font-bold">{{ latestSol.data.HWS?.av ?? '—' }} m/s</p>
          <p class="text-xs text-white/40 mt-1">média horária</p>
        </div>
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-2">Pressão</p>
          <p class="text-2xl font-bold">{{ latestSol.data.PRE?.av ?? '—' }}</p>
          <p class="text-xs text-white/40 mt-1">Pa · atmosfera fina</p>
        </div>
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-2">Direção do vento</p>
          <p class="text-2xl font-bold">{{ latestSol.data.WD?.most_common?.compass_point ?? '—' }}</p>
          <p class="text-xs text-white/40 mt-1">
            {{ latestSol.data.WD?.most_common?.compass_degrees ?? '—' }}° predominante
          </p>
        </div>
      </div>

      <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5 text-xs text-white/50">
        Período UTC: {{ latestSol.data.First_UTC?.split('T')[0] }} — {{ latestSol.data.Last_UTC?.split('T')[0] }}
      </div>
    </template>
  </div>
</template>
