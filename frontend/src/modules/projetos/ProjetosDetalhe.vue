<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useApi } from '../../composables/useApi.js'

const route = useRoute()
const router = useRouter()

const { data: project, loading, error } = useApi({
  immediate: true,
  url: () => `/techport/projects/${route.params.id}`,
  transform: (data) => data.project ?? data,
})

const timelineStatus = computed(() => {
  if (!project.value) return null
  if (project.value.endDate) return { label: 'Concluído', color: 'emerald' }
  return { label: 'Em andamento', color: 'blue' }
})

const formattedStart = computed(() => {
  if (!project.value) return '—'
  return project.value.startDateString ?? project.value.startDate?.split('T')[0] ?? '—'
})

const formattedEnd = computed(() => {
  if (!project.value) return null
  return project.value.endDateString ?? project.value.endDate?.split('T')[0] ?? null
})
</script>

<template>
  <div class="min-h-full text-white">

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center justify-center gap-4 min-h-[60vh]">
      <div class="relative">
        <span class="size-12 rounded-full border-2 border-white/[0.06] border-t-blue-400 animate-spin block" />
        <span class="absolute inset-0 size-12 rounded-full border-2 border-transparent border-b-purple-400/40 animate-spin block" style="animation-duration: 2s" />
      </div>
      <p class="text-sm text-white/40">Carregando projeto...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="flex flex-col items-center justify-center gap-4 min-h-[60vh]">
      <div class="size-16 rounded-full bg-red-500/10 border border-red-500/20 flex items-center justify-center">
        <svg class="size-7 text-red-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
        </svg>
      </div>
      <p class="text-sm text-red-400/80">Falha ao carregar os dados ({{ error }})</p>
      <button @click="router.push('/projetos')" class="mt-2 text-xs text-white/40 hover:text-white/70 transition-colors">
        ← Voltar aos projetos
      </button>
    </div>

    <!-- Content -->
    <template v-else-if="project">

      <!-- Hero Section -->
      <div class="relative px-10 pt-8 pb-12 overflow-hidden">
        <!-- Gradient background -->
        <div class="absolute inset-0 bg-gradient-to-br from-blue-900/20 via-transparent to-purple-900/10 pointer-events-none" />
        <div class="absolute top-0 right-0 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl pointer-events-none" />

        <div class="relative">
          <!-- Breadcrumb + Back -->
          <div class="flex items-center gap-4 mb-8">
            <button
              @click="router.push('/projetos')"
              class="flex items-center gap-2 text-xs text-white/40 hover:text-white/70 transition-colors group"
            >
              <svg class="size-4 group-hover:-translate-x-0.5 transition-transform" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
              </svg>
              Voltar aos projetos
            </button>
            <span class="text-white/10">|</span>
            <span class="text-[10px] font-mono text-white/25">ID: {{ project.projectId ?? route.params.id }}</span>
          </div>

          <!-- Title area -->
          <div class="max-w-3xl">
            <div class="flex items-center gap-3 mb-4">
              <span v-if="timelineStatus" :class="[
                'text-[11px] px-3 py-1 rounded-full border font-medium',
                timelineStatus.color === 'emerald'
                  ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/25'
                  : 'bg-blue-500/15 text-blue-300 border-blue-500/25'
              ]">
                {{ timelineStatus.label }}
              </span>
              <span v-if="project.acronym" class="text-[11px] px-3 py-1 rounded-full border border-white/[0.1] bg-white/[0.04] text-white/50">
                {{ project.acronym }}
              </span>
            </div>

            <h1 class="text-4xl font-bold tracking-tight leading-tight mb-4">
              {{ project.title ?? project.projectTitle }}
            </h1>

            <p v-if="project.leadOrganization?.organizationName" class="text-sm text-white/50 flex items-center gap-2">
              <svg class="size-4 text-white/30" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21" />
              </svg>
              {{ project.leadOrganization.organizationName }}
            </p>
          </div>
        </div>
      </div>

      <!-- Timeline bar -->
      <div class="px-10 mb-10">
        <div class="flex items-center gap-4 p-4 rounded-2xl bg-white/[0.02] border border-white/[0.06]">
          <div class="flex items-center gap-3 flex-1">
            <div class="size-8 rounded-lg bg-blue-500/10 flex items-center justify-center">
              <svg class="size-4 text-blue-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
              </svg>
            </div>
            <div>
              <p class="text-[10px] uppercase tracking-widest text-white/30 mb-0.5">Início</p>
              <p class="text-sm font-medium">{{ formattedStart }}</p>
            </div>
          </div>

          <!-- Timeline connector -->
          <div class="flex-1 flex items-center gap-2">
            <div class="flex-1 h-px bg-gradient-to-r from-blue-500/40 to-emerald-500/40" />
            <div class="size-2 rounded-full" :class="timelineStatus?.color === 'emerald' ? 'bg-emerald-400' : 'bg-blue-400 animate-pulse'" />
            <div class="flex-1 h-px bg-gradient-to-r from-emerald-500/40 to-white/[0.06]" />
          </div>

          <div class="flex items-center gap-3 flex-1 justify-end">
            <div>
              <p class="text-[10px] uppercase tracking-widest text-white/30 mb-0.5 text-right">Término</p>
              <p class="text-sm font-medium text-right">{{ formattedEnd ?? 'Em andamento' }}</p>
            </div>
            <div class="size-8 rounded-lg bg-emerald-500/10 flex items-center justify-center">
              <svg class="size-4 text-emerald-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Main content - Two columns -->
      <div class="px-10 pb-12">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">

          <!-- Left column: Description + Benefits (2/3) -->
          <div class="lg:col-span-2 space-y-8">

            <!-- Description -->
            <section v-if="project.description">
              <div class="flex items-center gap-2 mb-4">
                <div class="w-1 h-5 rounded-full bg-blue-400" />
                <h2 class="text-sm font-semibold uppercase tracking-wider text-white/60">Descrição</h2>
              </div>
              <div class="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6">
                <p class="text-sm text-white/70 leading-relaxed whitespace-pre-line">{{ project.description }}</p>
              </div>
            </section>

            <!-- Benefits -->
            <section v-if="project.benefits">
              <div class="flex items-center gap-2 mb-4">
                <div class="w-1 h-5 rounded-full bg-emerald-400" />
                <h2 class="text-sm font-semibold uppercase tracking-wider text-white/60">Benefícios</h2>
              </div>
              <div class="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6">
                <div class="text-sm text-white/70 leading-relaxed prose-invert" v-html="project.benefits" />
              </div>
            </section>

            <!-- Technology Areas -->
            <section v-if="project.primaryTas?.length">
              <div class="flex items-center gap-2 mb-4">
                <div class="w-1 h-5 rounded-full bg-purple-400" />
                <h2 class="text-sm font-semibold uppercase tracking-wider text-white/60">Áreas Tecnológicas</h2>
              </div>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="ta in project.primaryTas"
                  :key="ta.id"
                  class="text-xs px-3 py-1.5 rounded-xl bg-purple-500/10 text-purple-300 border border-purple-500/20 hover:bg-purple-500/15 transition-colors"
                >
                  {{ ta.title }}
                </span>
              </div>
            </section>
          </div>

          <!-- Right column: Metadata sidebar (1/3) -->
          <div class="space-y-5">

            <!-- Quick facts card -->
            <div class="rounded-2xl border border-white/[0.06] bg-white/[0.02] overflow-hidden">
              <div class="px-5 py-4 border-b border-white/[0.06] bg-white/[0.02]">
                <h3 class="text-xs font-semibold uppercase tracking-wider text-white/50">Informações</h3>
              </div>
              <div class="divide-y divide-white/[0.04]">
                <div class="px-5 py-4">
                  <p class="text-[10px] uppercase tracking-widest text-white/30 mb-1">ID do Projeto</p>
                  <p class="text-sm font-mono">{{ project.projectId }}</p>
                </div>
                <div v-if="project.leadOrganization" class="px-5 py-4">
                  <p class="text-[10px] uppercase tracking-widest text-white/30 mb-1">Centro NASA</p>
                  <p class="text-sm">{{ project.leadOrganization.organizationName ?? '—' }}</p>
                </div>
                <div v-if="project.responsibleMd" class="px-5 py-4">
                  <p class="text-[10px] uppercase tracking-widest text-white/30 mb-1">Diretoria</p>
                  <p class="text-sm">{{ project.responsibleMd.organizationName ?? '—' }}</p>
                </div>
                <div class="px-5 py-4">
                  <p class="text-[10px] uppercase tracking-widest text-white/30 mb-1">Status</p>
                  <p class="text-sm">{{ project.statusDescription ?? (project.endDate ? 'Concluído' : 'Ativo') }}</p>
                </div>
                <div v-if="project.website" class="px-5 py-4">
                  <p class="text-[10px] uppercase tracking-widest text-white/30 mb-1">Website</p>
                  <a :href="project.website" target="_blank" class="text-sm text-blue-400 hover:text-blue-300 transition-colors truncate block">
                    {{ project.website }}
                  </a>
                </div>
              </div>
            </div>

            <!-- Program info -->
            <div v-if="project.program" class="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-5">
              <p class="text-[10px] uppercase tracking-widest text-white/30 mb-2">Programa</p>
              <p class="text-sm font-medium">{{ project.program.title ?? '—' }}</p>
              <p v-if="project.program.acronym" class="text-xs text-white/40 mt-1">{{ project.program.acronym }}</p>
            </div>

            <!-- Destinations -->
            <div v-if="project.destinations?.length" class="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-5">
              <p class="text-[10px] uppercase tracking-widest text-white/30 mb-3">Destinos</p>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="dest in project.destinations"
                  :key="dest"
                  class="text-[11px] px-2.5 py-1 rounded-lg bg-white/[0.04] text-white/60 border border-white/[0.08]"
                >
                  {{ dest }}
                </span>
              </div>
            </div>

          </div>
        </div>
      </div>

    </template>
  </div>
</template>
