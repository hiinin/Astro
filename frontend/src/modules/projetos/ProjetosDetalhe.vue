<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const project = ref(null)
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await fetch(`/api/techport/projects/${route.params.id}`)
    if (!res.ok) throw new Error(res.status)
    const data = await res.json()
    project.value = data.project ?? data
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="min-h-full px-10 py-8 text-white">
    <div v-if="loading" class="flex items-center gap-3 text-sm text-white/40 py-16">
      <span class="size-4 rounded-full border-2 border-white/10 border-t-blue-400 animate-spin" />
      Carregando...
    </div>

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar os dados ({{ error }}).</p>

    <template v-else-if="project">
      <header class="mb-8">
        <nav class="mb-3 text-xs text-white/40">
          <router-link to="/" class="hover:text-white/70 transition-colors">/ rotas</router-link>
          <span> › </span>
          <router-link to="/projetos" class="hover:text-white/70 transition-colors">Projetos</router-link>
          <span> › {{ project.projectId ?? route.params.id }}</span>
        </nav>
        <h1 class="text-3xl font-bold mb-2">{{ project.title ?? project.projectTitle }}</h1>
        <p v-if="project.acronym" class="text-sm text-white/40">{{ project.acronym }}</p>
      </header>

      <div class="grid grid-cols-3 gap-4 mb-6">
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Centro NASA</p>
          <p class="text-sm">{{ project.leadOrganization?.organizationName ?? '—' }}</p>
        </div>
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Data de Início</p>
          <p class="text-sm">{{ project.startDateString ?? project.startDate?.split('T')[0] ?? '—' }}</p>
        </div>
        <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
          <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Data de Término</p>
          <p class="text-sm">{{ project.endDateString ?? project.endDate?.split('T')[0] ?? 'Em andamento' }}</p>
        </div>
      </div>

      <div class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5 mb-6">
        <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Descrição</p>
        <p class="text-sm text-white/70 leading-relaxed">{{ project.description ?? '—' }}</p>
      </div>

      <div v-if="project.benefits" class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5 mb-6">
        <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Benefícios</p>
        <p class="text-sm text-white/70 leading-relaxed" v-html="project.benefits" />
      </div>

      <div v-if="project.primaryTas?.length" class="rounded-xl border border-white/[0.08] bg-white/[0.03] p-5">
        <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Áreas Tecnológicas</p>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="ta in project.primaryTas"
            :key="ta.id"
            class="text-xs px-2 py-0.5 rounded bg-blue-500/10 text-blue-300 border border-blue-500/20"
          >
            {{ ta.title }}
          </span>
        </div>
      </div>
    </template>
  </div>
</template>
