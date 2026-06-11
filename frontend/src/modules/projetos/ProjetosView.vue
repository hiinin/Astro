<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiFetch } from '../../composables/useApi.js'

const router = useRouter()
const projects = ref([])
const totalCount = ref(0)
const loading = ref(false)
const error = ref(null)
const status = ref('')
const search = ref('')

const BATCH_SIZE = 15

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return projects.value
  return projects.value.filter((p) =>
    [p.title, p.acronym, String(p.projectId)]
      .filter(Boolean)
      .some((v) => String(v).toLowerCase().includes(q)),
  )
})

async function fetchProjectDetail(item) {
  try {
    const data = await apiFetch(`/techport/projects/${item.projectId}`)
    const p = data.project ?? data
    return {
      projectId: p.projectId ?? item.projectId,
      title: p.title,
      acronym: p.acronym || null,
      description: p.description || null,
      startDate: p.startDate,
      endDate: p.endDate,
      statusDescription: p.statusDescription || null,
      leadOrganization: p.leadOrganization?.organizationName || null,
      lastUpdated: item.lastUpdated,
    }
  } catch {
    return { projectId: item.projectId, lastUpdated: item.lastUpdated }
  }
}

async function load() {
  loading.value = true
  error.value = null
  projects.value = []
  status.value = 'Consultando catálogo da NASA Techport...'

  try {
    const data = await apiFetch('/techport/projects')
    const list = (data.projects ?? []).slice(0, BATCH_SIZE)
    totalCount.value = data.totalCount ?? data.projects?.length ?? 0
    status.value = `Carregando detalhes de ${list.length} projetos recentes...`
    projects.value = await Promise.all(list.map(fetchProjectDetail))
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
    status.value = ''
  }
}

function statusColor(project) {
  if (project.endDate) return 'bg-emerald-500/15 text-emerald-300 border-emerald-500/25'
  return 'bg-blue-500/15 text-blue-300 border-blue-500/25'
}

function statusLabel(project) {
  if (project.statusDescription) return project.statusDescription
  return project.endDate ? 'Concluído' : 'Em andamento'
}

onMounted(load)
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">

    <!-- Hero Header -->
    <header class="mb-10 relative">
      <div class="absolute -top-4 -left-4 size-32 bg-blue-500/10 rounded-full blur-3xl pointer-events-none" />
      <div class="relative">
        <div class="flex items-center gap-3 mb-4">
          <div class="size-10 rounded-xl bg-gradient-to-br from-blue-500/20 to-purple-500/20 border border-white/[0.08] flex items-center justify-center">
            <svg class="size-5 text-blue-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 1.5m-.5-1.5h-9.5m0 0-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6" />
            </svg>
          </div>
          <div>
            <h1 class="text-3xl font-bold tracking-tight">Projetos NASA</h1>
          </div>
        </div>

        <!-- Stats bar -->
        <div class="flex items-center gap-6 mt-6 pb-6 border-b border-white/[0.06]">
          <div class="flex items-center gap-2">
            <span class="size-2 rounded-full bg-blue-400 animate-pulse" />
            <span class="text-xs text-white/50">{{ totalCount.toLocaleString('pt-BR') }} projetos no catálogo</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="size-2 rounded-full bg-emerald-400" />
            <span class="text-xs text-white/50">{{ filtered.length }} exibidos</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center gap-4 py-24">
      <div class="relative">
        <span class="size-10 rounded-full border-2 border-white/[0.06] border-t-blue-400 animate-spin block" />
        <span class="absolute inset-0 size-10 rounded-full border-2 border-transparent border-b-purple-400/50 animate-spin block" style="animation-duration: 1.5s" />
      </div>
      <p class="text-sm text-white/40">{{ status }}</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="flex flex-col items-center gap-4 py-24">
      <div class="size-14 rounded-full bg-red-500/10 border border-red-500/20 flex items-center justify-center">
        <svg class="size-6 text-red-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
        </svg>
      </div>
      <p class="text-sm text-red-400/80">Falha ao carregar os dados ({{ error }})</p>
    </div>

    <!-- Content -->
    <template v-else>
      <!-- Search -->
      <form class="flex gap-3 mb-10 w-full">
        <input
          v-model="search"
          placeholder="Filtrar por nome, acrônimo ou ID..."
          class="flex-1 bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm text-white placeholder-white/30 outline-none focus:border-white/20 transition-colors"
        />
        <button
          type="button"
          class="px-5 py-2.5 bg-blue-500/20 border border-blue-500/30 text-blue-300 text-sm rounded-lg hover:bg-blue-500/30 transition-colors"
        >
          Buscar
        </button>
      </form>

      <!-- Grid de cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
        <div
          v-for="project in filtered"
          :key="project.projectId"
          class="group relative rounded-2xl border border-white/[0.07] bg-white/[0.02] p-6 cursor-pointer hover:border-white/[0.15] hover:bg-white/[0.04] transition-all duration-300 hover:-translate-y-0.5 hover:shadow-2xl hover:shadow-blue-900/10"
          @click="router.push(`/projetos/${project.projectId}`)"
        >
          <!-- Top row: ID + Status -->
          <div class="flex items-center justify-between mb-4">
            <span class="text-[10px] font-mono text-white/30 bg-white/[0.04] px-2 py-0.5 rounded">#{{ project.projectId }}</span>
            <span :class="['text-[10px] px-2.5 py-0.5 rounded-full border', statusColor(project)]">
              {{ statusLabel(project) }}
            </span>
          </div>

          <!-- Title -->
          <h3 class="text-sm font-semibold text-white/90 leading-snug mb-2 line-clamp-2 group-hover:text-white transition-colors">
            {{ project.title ?? 'Sem título' }}
          </h3>

          <!-- Description snippet -->
          <p v-if="project.description" class="text-xs text-white/35 line-clamp-2 leading-relaxed mb-4">
            {{ project.description }}
          </p>
          <div v-else class="mb-4" />

          <!-- Footer info -->
          <div class="flex items-center justify-between pt-4 border-t border-white/[0.05]">
            <div class="flex items-center gap-1.5">
              <svg class="size-3 text-white/25" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21" />
              </svg>
              <span class="text-[10px] text-white/30 truncate max-w-[120px]">{{ project.leadOrganization ?? '—' }}</span>
            </div>
            <span class="text-[10px] text-white/25">{{ project.startDate?.split('T')[0] ?? '—' }}</span>
          </div>

          <!-- Hover arrow -->
          <div class="absolute top-5 right-5 opacity-0 group-hover:opacity-100 transition-opacity">
            <svg class="size-4 text-white/30" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Empty filter state -->
      <div v-if="filtered.length === 0 && projects.length > 0" class="text-center py-16">
        <p class="text-sm text-white/30">Nenhum projeto encontrado para "<span class="text-white/50">{{ search }}</span>"</p>
      </div>
    </template>
  </div>
</template>
