<script setup>
import { useRoute } from 'vue-router'
import { useApi } from '../../composables/useApi.js'

const route = useRoute()
const { data: event, loading, error } = useApi({
  immediate: true,
  url: () => `/eonet/events/${route.params.id}`,
})
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <template v-else-if="event">
      <header class="mb-8">
        <nav class="mb-3 text-xs text-white/40">
          <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
          <span> › </span>
          <router-link to="/eventos-naturais" class="hover:text-white/70 transition-colors">Eventos Naturais</router-link>
          <span> › {{ event.id }}</span>
        </nav>
        <div class="flex items-start justify-between gap-4">
          <div>
            <h1 class="text-3xl font-bold mb-2">{{ event.title }}</h1>
            <p class="text-sm text-white/40">ID: {{ event.id }}</p>
          </div>
          <span
            class="text-xs px-2 py-1 rounded border"
            :class="event.closed ? 'text-white/30 bg-white/5 border-white/10' : 'text-green-400 bg-green-500/10 border-green-500/20'"
          >
            {{ event.closed ? 'Encerrado' : 'Ativo' }}
          </span>
        </div>
      </header>

      <div class="grid grid-cols-4 gap-4 mb-6">
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Categorias</p>
          <div class="flex flex-wrap gap-1.5">
            <span
              v-for="cat in event.categories"
              :key="cat.id"
              class="text-xs px-2 py-0.5 rounded bg-blue-500/10 text-blue-300 border border-blue-500/20"
            >
              {{ cat.title }}
            </span>
          </div>
        </div>
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Fontes</p>
          <div class="space-y-1">
            <a
              v-for="src in event.sources"
              :key="src.id"
              :href="src.url"
              target="_blank"
              class="text-xs text-blue-400 hover:underline block truncate"
            >
              {{ src.id }}
            </a>
          </div>
        </div>
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Ocorrências</p>
          <p class="text-3xl font-bold">{{ event.geometry?.length ?? 0 }}</p>
          <p class="text-xs text-white/40 mt-1">registros geoespaciais</p>
        </div>
      </div>

      <div class="rounded-xl border border-white/[0.08] overflow-hidden">
        <p class="px-5 py-4 border-b border-white/[0.08] text-[11px] uppercase tracking-widest text-white/40">
          Registros Geoespaciais
        </p>
        <table class="w-full text-xs">
          <thead>
            <tr class="text-white/35 border-b border-white/[0.08]">
              <th class="px-4 py-2.5 text-left font-medium">Data</th>
              <th class="px-4 py-2.5 text-left font-medium">Tipo</th>
              <th class="px-4 py-2.5 text-left font-medium">Coordenadas</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(geo, i) in event.geometry"
              :key="i"
              class="border-b border-white/[0.04] last:border-0 hover:bg-white/[0.02]"
            >
              <td class="px-4 py-3 text-white/60">{{ geo.date?.split('T')[0] }}</td>
              <td class="px-4 py-3 text-white/60">{{ geo.type }}</td>
              <td class="px-4 py-3 text-white/60 font-mono">
                {{ Array.isArray(geo.coordinates) ? geo.coordinates.slice(0, 2).join(', ') : '—' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>
