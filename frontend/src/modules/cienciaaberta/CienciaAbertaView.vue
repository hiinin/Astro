<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '../../composables/useApi.js'

const query = ref('')
const studies = ref([])
const total = ref(0)
const selected = ref(null)
const showRaw = ref(false)
const { loading, error, run } = useApi()

const PAGE_SIZE = 50

function formatMission(mission) {
  if (!mission || typeof mission !== 'object') return null
  const name = mission.Name?.trim()
  if (!name) return null
  const year = mission['Start Date']?.match(/\d{4}/)?.[0]
  return year ? `${name} (${year})` : name
}

function normalize(hit) {
  const src = hit._source ?? hit
  const title = src['Project Title']?.trim() || src['Study Title']?.trim() || 'Sem título'

  return {
    id: src['Study Identifier'] ?? hit._id,
    title,
    mission: formatMission(src.Mission),
    program: src['Flight Program']?.trim() || null,
    area: src['Study Assay Measurement Type']?.trim() || src['Material Type']?.trim() || null,
    description: src['Study Description']?.trim() || src['Study Protocol Description']?.trim() || null,
    raw: src,
  }
}

function selectStudy(study) {
  selected.value = study
  showRaw.value = false
}

async function load() {
  const q = query.value.trim()
  const url = q ? `/osdr/search?q=${encodeURIComponent(q)}` : '/osdr/search'
  const json = await run(url)

  if (!json) {
    studies.value = []
    total.value = 0
    return
  }

  total.value = json.hits?.total ?? 0
  studies.value = (json.hits?.hits ?? [])
    .map(normalize)
    .filter((s) => s.mission || s.program || (s.description && s.title.length > 20))
}

onMounted(load)
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <nav class="mb-3 text-xs text-white/40">
        <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
        <span> › Ciência Aberta</span>
      </nav>
      <h1 class="text-2xl font-bold mb-1">Ciência Aberta</h1>
      <p class="text-sm text-white/40 max-w-xl">
        Estudos científicos publicados no repositório aberto da NASA (OSDR).
      </p>
    </header>

    <form @submit.prevent="load" class="flex gap-3 mb-6">
      <input
        v-model="query"
        placeholder="Buscar estudo (opcional)..."
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
      Carregando estudos...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar ({{ error }}).</p>

    <p v-else-if="!studies.length" class="text-sm text-white/40 py-16">Nenhum estudo encontrado.</p>

    <div v-else class="flex gap-6 items-start">
      <div class="flex-1 min-w-0 rounded-xl border border-white/[0.08] overflow-hidden">
        <div class="px-5 py-3 border-b border-white/[0.08] text-xs text-white/35">
          {{ studies.length }} de {{ total.toLocaleString('pt-BR') }} estudos
        </div>
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-white/[0.08] text-left text-xs text-white/40 uppercase tracking-wider">
              <th class="px-5 py-3 font-medium">Estudo</th>
              <th class="px-5 py-3 font-medium">Missão</th>
              <th class="px-5 py-3 font-medium">Programa</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="study in studies"
              :key="study.id"
              class="border-b border-white/[0.05] last:border-0 cursor-pointer transition-colors"
              :class="selected?.id === study.id ? 'bg-blue-500/10' : 'hover:bg-white/[0.02]'"
              @click="selectStudy(study)"
            >
              <td class="px-5 py-3.5 font-medium max-w-sm">
                <p class="line-clamp-2">{{ study.title }}</p>
              </td>
              <td class="px-5 py-3.5 text-white/55 text-xs whitespace-nowrap">{{ study.mission ?? '—' }}</td>
              <td class="px-5 py-3.5 text-white/55 text-xs max-w-[180px] truncate">{{ study.program ?? '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>


      <aside
        v-if="selected"
        class="w-96 shrink-0 rounded-xl border border-white/[0.08] bg-white/[0.02] overflow-hidden"
      >
        <div class="px-5 py-4 border-b border-white/[0.08]">
          <p class="text-[11px] uppercase tracking-widest text-white/35 mb-2">Detalhes</p>
          <h2 class="text-sm font-semibold leading-snug">{{ selected.title }}</h2>
        </div>

        <div class="px-5 py-4 space-y-3 text-xs">
          <div v-if="selected.mission">
            <p class="text-white/35 mb-0.5">Missão</p>
            <p class="text-white/70">{{ selected.mission }}</p>
          </div>
          <div v-if="selected.program">
            <p class="text-white/35 mb-0.5">Programa</p>
            <p class="text-white/70">{{ selected.program }}</p>
          </div>
          <div v-if="selected.area">
            <p class="text-white/35 mb-0.5">Área</p>
            <p class="text-white/70">{{ selected.area }}</p>
          </div>
          <div v-if="selected.description">
            <p class="text-white/35 mb-0.5">Resumo</p>
            <p class="text-white/60 leading-relaxed line-clamp-12">{{ selected.description }}</p>
          </div>
          <p v-if="selected.id" class="font-mono text-[10px] text-white/25 pt-1">{{ selected.id }}</p>
        </div>

        <div class="border-t border-white/[0.08]">
          <button
            type="button"
            class="w-full px-5 py-3 text-left text-xs text-white/45 hover:text-white/70 hover:bg-white/[0.02] transition-colors"
            @click="showRaw = !showRaw"
          >
            {{ showRaw ? 'Ocultar' : 'Ver' }} dados brutos (JSON)
          </button>
          <pre
            v-if="showRaw"
            class="px-5 pb-4 text-[10px] text-white/40 overflow-auto max-h-64 leading-relaxed"
          >{{ JSON.stringify(selected.raw, null, 2) }}</pre>
        </div>
      </aside>

      <div
        v-else
        class="w-96 shrink-0 rounded-xl border border-white/[0.06] border-dashed px-5 py-10 text-center text-xs text-white/30"
      >
        Selecione um estudo na lista para ver os detalhes.
      </div>
    </div>
  </div>
</template>
