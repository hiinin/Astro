<script setup>
import { ref, onMounted } from 'vue'
import { useRequest as useApi } from '../../composables'

const query = ref('')
const studies = ref([])
const total = ref(0)
const selected = ref(null)
const detailData = ref(null)
const showRaw = ref(false)
const { loading, error, run } = useApi()

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
    organism: src['Study Organism']?.trim() || null,
    factor: src['Study Factor Name']?.trim() || null,
    assayType: src['Study Assay Technology Type']?.trim() || null,
    platform: src['Study Assay Technology Platform']?.trim() || null,
    raw: src,
  }
}

async function selectStudy(study) {
  selected.value = study
  showRaw.value = false
  detailData.value = null

  if (study.id) {
    const meta = await run(`/osdr/study/meta/${study.id}`)
    if (meta) detailData.value = meta
  }
}

function closeDetail() {
  selected.value = null
  detailData.value = null
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
      <h1 class="text-4xl font-bold mb-1">Ciência Aberta</h1>
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

    <div v-if="loading && !selected" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando estudos...
    </div>

    <p v-else-if="error && !selected" class="text-sm text-red-400 py-16">Falha ao carregar ({{ error }}).</p>

    <p v-else-if="!studies.length && !selected" class="text-sm text-white/40 py-16">Nenhum estudo encontrado.</p>

    <!-- Split layout: cards + detail -->
    <div v-else class="flex gap-6 items-start">
      <!-- Left: study cards -->
      <div class="w-1/2 min-w-0 space-y-3 max-h-[calc(100vh-220px)] overflow-y-auto pr-2">
        <p class="text-xs text-white/35 mb-2">
          {{ studies.length }} de {{ total.toLocaleString('pt-BR') }} estudos
        </p>

        <div
          v-for="study in studies"
          :key="study.id"
          class="rounded-xl border p-4 cursor-pointer transition-all duration-200"
          :class="selected?.id === study.id
            ? 'border-blue-500/40 bg-blue-500/[0.08] shadow-lg shadow-blue-500/5'
            : 'border-white/[0.08] bg-white/[0.02] hover:border-white/[0.15] hover:bg-white/[0.04]'"
          @click="selectStudy(study)"
        >
          <h3 class="text-sm font-medium leading-snug mb-2 line-clamp-2"
              :class="selected?.id === study.id ? 'text-blue-200' : 'text-white/85'">
            {{ study.title }}
          </h3>

          <div class="flex flex-wrap gap-1.5">
            <span v-if="study.mission" class="px-2 py-0.5 rounded-md bg-blue-500/10 text-[10px] text-blue-300 border border-blue-500/20">
              {{ study.mission }}
            </span>
            <span v-if="study.program" class="px-2 py-0.5 rounded-md bg-purple-500/10 text-[10px] text-purple-300 border border-purple-500/20">
              {{ study.program }}
            </span>
            <span v-if="study.area" class="px-2 py-0.5 rounded-md bg-emerald-500/10 text-[10px] text-emerald-300 border border-emerald-500/20">
              {{ study.area }}
            </span>
          </div>

          <p v-if="study.description" class="mt-2 text-xs text-white/40 line-clamp-2 leading-relaxed">
            {{ study.description }}
          </p>
        </div>
      </div>

      <!-- Right: detail panel -->
      <div class="w-1/2 shrink-0 sticky top-8">
        <Transition name="fade" mode="out-in">
          <!-- Detail content -->
          <div
            v-if="selected"
            :key="selected.id"
            class="rounded-2xl border border-white/[0.1] bg-white/[0.02] overflow-hidden max-h-[calc(100vh-220px)] flex flex-col"
          >
            <!-- Header -->
            <div class="px-6 py-5 border-b border-white/[0.08] shrink-0">
              <div class="flex items-start justify-between gap-4">
                <div class="min-w-0">
                  <p class="text-[11px] uppercase tracking-widest text-blue-400/70 mb-1.5 font-medium">
                    Estudo {{ selected.id }}
                  </p>
                  <h2 class="text-base font-semibold leading-snug text-white/90">{{ selected.title }}</h2>
                </div>
                <button
                  @click="closeDetail"
                  class="shrink-0 size-8 flex items-center justify-center rounded-lg text-white/40 hover:text-white hover:bg-white/[0.06] transition-colors"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="size-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Scrollable body -->
            <div class="flex-1 overflow-y-auto px-6 py-5 space-y-5">
              <!-- Badges -->
              <div class="flex flex-wrap gap-2">
                <span v-if="selected.mission" class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-xs text-blue-300">
                  {{ selected.mission }}
                </span>
                <span v-if="selected.program" class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-xs text-purple-300">
                  {{ selected.program }}
                </span>
                <span v-if="selected.area" class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-300">
                  {{ selected.area }}
                </span>
                <span v-if="selected.organism" class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-xs text-amber-300">
                  {{ selected.organism }}
                </span>
              </div>

              <!-- Description -->
              <div v-if="selected.description" class="space-y-1.5">
                <p class="text-[11px] uppercase tracking-widest text-white/35 font-medium">Descrição</p>
                <p class="text-sm text-white/65 leading-relaxed">{{ selected.description }}</p>
              </div>

              <!-- Info grid -->
              <div class="grid grid-cols-2 gap-3">
                <div v-if="selected.factor" class="rounded-lg bg-white/[0.03] border border-white/[0.06] p-3">
                  <p class="text-[10px] uppercase tracking-widest text-white/35 mb-1">Fator de estudo</p>
                  <p class="text-sm text-white/70">{{ selected.factor }}</p>
                </div>
                <div v-if="selected.assayType" class="rounded-lg bg-white/[0.03] border border-white/[0.06] p-3">
                  <p class="text-[10px] uppercase tracking-widest text-white/35 mb-1">Tipo de ensaio</p>
                  <p class="text-sm text-white/70">{{ selected.assayType }}</p>
                </div>
                <div v-if="selected.platform" class="rounded-lg bg-white/[0.03] border border-white/[0.06] p-3">
                  <p class="text-[10px] uppercase tracking-widest text-white/35 mb-1">Plataforma</p>
                  <p class="text-sm text-white/70">{{ selected.platform }}</p>
                </div>
                <div v-if="selected.id" class="rounded-lg bg-white/[0.03] border border-white/[0.06] p-3">
                  <p class="text-[10px] uppercase tracking-widest text-white/35 mb-1">Identificador</p>
                  <p class="text-sm text-white/70 font-mono">{{ selected.id }}</p>
                </div>
              </div>

              <!-- Metadata from API -->
              <div v-if="detailData" class="space-y-1.5">
                <p class="text-[11px] uppercase tracking-widest text-white/35 font-medium">Metadados adicionais</p>
                <div class="rounded-lg bg-white/[0.03] border border-white/[0.06] p-4">
                  <pre class="text-[11px] text-white/50 overflow-auto max-h-48 leading-relaxed whitespace-pre-wrap">{{ JSON.stringify(detailData, null, 2) }}</pre>
                </div>
              </div>

              <!-- Loading detail indicator -->
              <div v-if="loading && !detailData" class="flex items-center gap-2 text-xs text-white/40">
                <span class="size-3 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
                Carregando metadados...
              </div>

              <!-- Raw JSON -->
              <div class="border-t border-white/[0.06] pt-4">
                <button
                  type="button"
                  class="text-xs text-white/40 hover:text-white/70 transition-colors"
                  @click="showRaw = !showRaw"
                >
                  {{ showRaw ? '▾ Ocultar' : '▸ Ver' }} dados brutos (JSON)
                </button>
                <pre
                  v-if="showRaw"
                  class="mt-3 text-[10px] text-white/40 overflow-auto max-h-64 leading-relaxed bg-white/[0.02] rounded-lg p-4 border border-white/[0.05]"
                >{{ JSON.stringify(selected.raw, null, 2) }}</pre>
              </div>
            </div>
          </div>

          <!-- Empty state -->
          <div
            v-else
            class="rounded-2xl border border-white/[0.06] border-dashed flex items-center justify-center py-20 text-center"
          >
            <div>
              <svg xmlns="http://www.w3.org/2000/svg" class="size-10 mx-auto mb-3 text-white/15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <p class="text-xs text-white/30">Selecione um estudo para ver os detalhes</p>
            </div>
          </div>
        </Transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
