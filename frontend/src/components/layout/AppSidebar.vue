<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const mainLinks = [
  {
    name: 'foto-do-dia',
    path: '/foto-do-dia',
    label: 'Foto do Dia',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>`
  },
  {
    name: 'asteroides',
    path: '/asteroides',
    label: 'Asteroides',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>`
  },
  {
    name: 'camera-terra',
    path: '/camera-terra',
    label: 'Câmera da Terra',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>`
  },
  {
    name: 'clima-marte',
    path: '/clima-marte',
    label: 'Clima em Marte',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41"/></svg>`
  },
  {
    name: 'imagens-terra',
    path: '/imagens-terra',
    label: 'Imagens da Terra',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>`
  },
  {
    name: 'rovers-marte',
    path: '/rovers-marte',
    label: 'Rovers em Marte',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>`
  },
  {
    name: 'clima-espacial',
    path: '/clima-espacial',
    label: 'Clima Espacial',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>`
  },
  {
    name: 'eventos-naturais',
    path: '/eventos-naturais',
    label: 'Eventos Naturais',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`
  },
  {
    name: 'satelites',
    path: '/satelites',
    label: 'Satélites',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 7 9 3 5 7l4 4"/><path d="m17 11 4 4-4 4-4-4"/><path d="m8 12 4 4 6-6-4-4Z"/><path d="m16 8 3-3"/><path d="M9 21a6 6 0 0 0-6-6"/></svg>`
  },
  {
    name: 'sistema-solar',
    path: '/sistema-solar',
    label: 'Sistema Solar',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(-30 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(30 12 12)"/></svg>`
  },
  {
    name: 'exoplanetas',
    path: '/exoplanetas',
    label: 'Exoplanetas',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="9"/><line x1="3" y1="12" x2="21" y2="12"/><path d="M12 3a9 9 0 0 1 0 18"/></svg>`
  },
  {
    name: 'ciencia-aberta',
    path: '/ciencia-aberta',
    label: 'Ciência Aberta',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v11m0 0h10m-10 0a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2m0-11v11M3 9h18"/></svg>`
  },
  {
    name: 'midias',
    path: '/midias',
    label: 'Mídias',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg>`
  },
  {
    name: 'projetos',
    path: '/projetos',
    label: 'Projetos',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>`
  },
  {
    name: 'techtransfer',
    path: '/techtransfer',
    label: 'TechTransfer',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4"/><path d="m6.8 15-3.5 2"/><path d="m20.7 17-3.5-2"/><path d="M6.8 9 3.3 7"/><path d="m20.7 7-3.5 2"/><circle cx="12" cy="12" r="4"/><path d="M12 18v4"/></svg>`
  },
]

function isActive(path) {
  return route.path.startsWith(path)
}
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-logo">
      <router-link to="/" aria-label="NASA">
        <img src="/imagens/logo-nasa.svg" alt="NASA" />
      </router-link>
    </div>

    <nav class="sidebar-nav">
      <ul>
        <li v-for="link in mainLinks" :key="link.name">
          <router-link
            :to="link.path"
            :class="['nav-item', { active: isActive(link.path) }]"
          >
            <span class="nav-icon" v-html="link.icon" />
            <span class="nav-label">{{ link.label }}</span>
          </router-link>
        </li>
      </ul>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  width: 220px;
  min-width: 220px;
  height: 100vh;
  background-color: #060B17;
  border-right: 1px solid rgba(255, 255, 255, 0.06);
  overflow-y: auto;
  overflow-x: hidden;
  
  
}

.sidebar-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.sidebar-logo img {
  height: 60px;
  width: auto;
  object-fit: contain;
}

.sidebar-nav {
  flex: 1;
  padding: 8px 0;
  
}

.sidebar-nav ul {
  list-style: none;
  margin: 0;
  padding: 0;
 
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px;
  color: rgba(255, 255, 255, 0.55);
  text-decoration: none;
  font-size: 13px;
  font-weight: 400;
  transition: color 0.15s, background-color 0.15s;
  border-radius: 0;
  cursor: pointer;
}

.nav-item:hover {
  color: rgba(255, 255, 255, 0.9);
  background-color: #101B2E;
}

.nav-item.active {
  color: #ffffff;
  background-color: #0F1C35;
  border-left: 2px solid #4d9fff;
}

.nav-icon {
  display: flex;
  align-items: center;
  flex-shrink: 0;
  opacity: 0.8;
}

.nav-item.active .nav-icon {
  opacity: 1;
}

.nav-label {
  line-height: 1.3;
}
</style>
