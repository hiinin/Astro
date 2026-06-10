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
      startDate: p.startDate,
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

onMounted(load)
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <header class="mb-8">
      <nav class="mb-3 text-xs text-white/40">
        <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
        <span> › Projetos</span>
      </nav>
      <h1 class="text-2xl font-bold mb-1">Projetos NASA</h1>
      <p class="text-sm text-white/40">Portfólio de tecnologias e projetos via NASA Techport.</p>
    </header>

 

    <div v-if="loading" class="flex flex-col items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      <p>{{ status }}</p>
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <template v-else>
      <div class="flex items-center justify-between mb-5">
        <input
          v-model="search"
          placeholder="Filtrar projetos carregados..."
          class="w-80 bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm text-white placeholder-white/30 outline-none focus:border-white/20 transition-colors"
        />
        <p class="text-xs text-white/40">
          {{ filtered.length }} exibidos · {{ totalCount.toLocaleString('pt-BR') }} no catálogo
        </p>
      </div>

      <div class="rounded-xl border border-white/[0.08] overflow-hidden">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-white/[0.08] text-left text-xs text-white/40 uppercase tracking-wider">
              <th class="px-5 py-3 font-medium">ID</th>
              <th class="px-5 py-3 font-medium">Título</th>
              <th class="px-5 py-3 font-medium">Acrônimo</th>
              <th class="px-5 py-3 font-medium">Início</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="project in filtered"
              :key="project.projectId"
              class="border-b border-white/[0.05] last:border-0 hover:bg-white/[0.03] cursor-pointer transition-colors"
              @click="router.push(`/projetos/${project.projectId}`)"
            >
              <td class="px-5 py-3.5 text-white/40 font-mono text-xs">{{ project.projectId }}</td>
              <td class="px-5 py-3.5 font-medium max-w-md truncate">{{ project.title ?? '—' }}</td>
              <td class="px-5 py-3.5 text-white/50 text-xs">{{ project.acronym ?? '—' }}</td>
              <td class="px-5 py-3.5 text-white/50 text-xs">{{ project.startDate ?? '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>
