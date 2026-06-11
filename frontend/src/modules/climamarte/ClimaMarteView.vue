<script setup>
import { computed } from 'vue'
import { useRequest as useApi } from '../../composables'

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
      <h1 class="text-4xl font-bold mb-1">Clima em Marte</h1>
      <p class="text-sm text-white/40">Dados meteorológicos da missão InSight na superfície marciana.</p>
    </header>

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <template v-else-if="latestSol">
      <div class="rounded-2xl border border-white/[0.08] overflow-hidden">
        <table class="w-full text-xs">
          <thead>
            <tr class="bg-white/[0.04] border-b border-white/[0.08] text-white/40 uppercase tracking-widest text-[10px] font-medium">
              <th class="px-5 py-3 text-left">Métrica</th>
              <th class="px-5 py-3 text-right">Média</th>
              <th class="px-5 py-3 text-right">Mínimo</th>
              <th class="px-5 py-3 text-right">Máximo</th>
              <th class="px-5 py-3 text-left">Observação</th>
            </tr>
          </thead>
          <tbody>
            <tr class="border-b border-white/[0.04] hover:bg-white/[0.03] transition-colors">
              <td class="px-5 py-3 text-white/50 uppercase tracking-widest text-[10px]">Temperatura</td>
              <td class="px-5 py-3 text-right font-mono text-white/80 font-medium text-sm">
                {{ latestSol.data.AT?.av ?? '—' }}°C
              </td>
              <td class="px-5 py-3 text-right font-mono text-white/50">
                {{ latestSol.data.AT?.mn ?? '—' }}°C
              </td>
              <td class="px-5 py-3 text-right font-mono text-white/50">
                {{ latestSol.data.AT?.mx ?? '—' }}°C
              </td>
              <td class="px-5 py-3 text-white/35">Temperatura do ar (AT)</td>
            </tr>
            <tr class="border-b border-white/[0.04] hover:bg-white/[0.03] transition-colors">
              <td class="px-5 py-3 text-white/50 uppercase tracking-widest text-[10px]">Vento</td>
              <td class="px-5 py-3 text-right font-mono text-white/80 font-medium text-sm">
                {{ latestSol.data.HWS?.av ?? '—' }} m/s
              </td>
              <td class="px-5 py-3 text-right font-mono text-white/50">
                {{ latestSol.data.HWS?.mn ?? '—' }} m/s
              </td>
              <td class="px-5 py-3 text-right font-mono text-white/50">
                {{ latestSol.data.HWS?.mx ?? '—' }} m/s
              </td>
              <td class="px-5 py-3 text-white/35">Velocidade horizontal do vento</td>
            </tr>
            <tr class="border-b border-white/[0.04] hover:bg-white/[0.03] transition-colors">
              <td class="px-5 py-3 text-white/50 uppercase tracking-widest text-[10px]">Pressão</td>
              <td class="px-5 py-3 text-right font-mono text-white/80 font-medium text-sm">
                {{ latestSol.data.PRE?.av ?? '—' }} Pa
              </td>
              <td class="px-5 py-3 text-right font-mono text-white/50">
                {{ latestSol.data.PRE?.mn ?? '—' }} Pa
              </td>
              <td class="px-5 py-3 text-right font-mono text-white/50">
                {{ latestSol.data.PRE?.mx ?? '—' }} Pa
              </td>
              <td class="px-5 py-3 text-white/35">Pressão atmosférica (PRE)</td>
            </tr>
            <tr class="hover:bg-white/[0.03] transition-colors">
              <td class="px-5 py-3 text-white/50 uppercase tracking-widest text-[10px]">Direção do vento</td>
              <td class="px-5 py-3 text-right font-mono text-white/80 font-medium text-sm">
                {{ latestSol.data.WD?.most_common?.compass_point ?? '—' }}
              </td>
              <td class="px-5 py-3 text-right font-mono text-white/50">—</td>
              <td class="px-5 py-3 text-right font-mono text-white/50">—</td>
              <td class="px-5 py-3 text-white/35">
                {{ latestSol.data.WD?.most_common?.compass_degrees ?? '—' }}° predominante
              </td>
            </tr>
          </tbody>
        </table>

        <div class="flex items-center justify-between px-5 py-3 border-t border-white/[0.06] bg-white/[0.02]">
          <span class="text-[11px] text-white/30 uppercase tracking-widest">
            Sol {{ latestSol.key }} · {{ latestSol.data.Season ?? '—' }}
          </span>
          <span class="text-[11px] text-white/25">
            {{ latestSol.data.First_UTC?.split('T')[0] }} — {{ latestSol.data.Last_UTC?.split('T')[0] }}
          </span>
        </div>
      </div>
    </template>
  </div>
</template>