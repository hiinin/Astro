<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { apiFetch } from '../../composables'
import { osdDetailTitle, osdDetailRows, OSDR_TYPE_LABELS } from '../../composables'

const route = useRoute()
const type = route.params.type
const id = decodeURIComponent(route.params.id)

const data = ref(null)
const loading = ref(true)
const error = ref(null)

const typeLabel = OSDR_TYPE_LABELS[type] ?? type

onMounted(async () => {
  try {
    data.value = await apiFetch(`/osdr/${type}/${encodeURIComponent(id)}`)
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

    <p v-else-if="error" class="text-sm text-red-400 py-16">Falha ao carregar ({{ error }}).</p>

    <template v-else-if="data">
      <header class="mb-8">
        <p class="text-[11px] uppercase tracking-widest text-blue-400/70 mb-2 font-medium">
          {{ typeLabel }}
        </p>
        <h1 class="text-3xl font-bold mb-2">{{ osdDetailTitle(data) }}</h1>
        <p class="text-xs text-white/35 font-mono">{{ id }}</p>
      </header>

      <!-- Descrição -->
      <div v-if="data.description" class="rounded-xl border border-white/[0.08] bg-white/[0.02] p-5 mb-6">
        <p class="text-[11px] uppercase tracking-widest text-white/40 mb-3">Descrição</p>
        <p class="text-sm text-white/70 leading-relaxed">{{ data.description }}</p>
      </div>

      <!-- Dados formatados -->
      <div class="rounded-xl border border-white/[0.08] overflow-hidden">
        <p class="px-5 py-4 border-b border-white/[0.08] text-[11px] uppercase tracking-widest text-white/40">
          Propriedades
        </p>
        <table class="w-full text-xs">
          <tbody>
            <tr
              v-for="row in osdDetailRows(data)"
              :key="row.key"
              class="border-b border-white/[0.04] last:border-0"
            >
              <td class="px-5 py-3 text-white/40 w-1/3 align-top">{{ row.label }}</td>
              <td class="px-5 py-3 text-white/70">
                <template v-if="row.link">
                  <router-link
                    :to="`/ciencia-aberta/${row.link.type}/${encodeURIComponent(row.link.id)}`"
                    class="text-blue-400 hover:text-blue-300"
                  >
                    {{ row.link.id }}
                  </router-link>
                </template>
                <template v-else-if="row.links">
                  <span v-for="(lnk, li) in row.links" :key="li">
                    <router-link
                      :to="`/ciencia-aberta/${lnk.type}/${encodeURIComponent(lnk.id)}`"
                      class="text-blue-400 hover:text-blue-300"
                    >{{ lnk.id }}</router-link>
                    <span v-if="li < row.links.length - 1" class="text-white/20">, </span>
                  </span>
                </template>
                <template v-else>{{ row.value }}</template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>
