<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const projects = ref(null)
const loading = ref(true)
const error = ref(null)
const search = ref('')

onMounted(async () => {
  try {
    const res = await fetch('/api/techport/projects')
    if (!res.ok) throw new Error(res.status)
    const data = await res.json()
    projects.value = data.projects ?? data
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

const filtered = () =>
  (projects.value ?? []).filter(p =>
    String(p.title ?? p.projectTitle ?? p.acronym ?? p.id ?? '').toLowerCase().includes(search.value.toLowerCase())
  )
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

    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <template v-else-if="projects">
      <div class="flex items-center justify-between mb-5">
        <input
          v-model="search"
          placeholder="Buscar por título ou acrônimo..."
          class="w-80 bg-white/[0.04] border border-white/[0.08] rounded-lg px-4 py-2.5 text-sm text-white placeholder-white/30 outline-none focus:border-white/20 transition-colors"
        />
        <p class="text-xs text-white/40">{{ filtered().length }} projetos</p>
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
              v-for="project in filtered().slice(0, 60)"
              :key="project.projectId ?? project.id"
              class="border-b border-white/[0.05] last:border-0 hover:bg-white/[0.03] cursor-pointer transition-colors"
              @click="router.push(`/projetos/${project.projectId ?? project.id}`)"
            >
              <td class="px-5 py-3.5 text-white/40 font-mono text-xs">{{ project.projectId ?? project.id }}</td>
              <td class="px-5 py-3.5 font-medium max-w-sm truncate">{{ project.title ?? project.projectTitle ?? '—' }}</td>
              <td class="px-5 py-3.5 text-white/50 text-xs">{{ project.acronym ?? '—' }}</td>
              <td class="px-5 py-3.5 text-white/50 text-xs">{{ project.startDateString ?? project.startDate?.split('T')[0] ?? '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>
