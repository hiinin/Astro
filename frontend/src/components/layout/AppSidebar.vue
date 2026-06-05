<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const mainLinks = [
  {
    name: 'asteroides',
    path: '/asteroides',
    label: 'Asteroides',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>`
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
