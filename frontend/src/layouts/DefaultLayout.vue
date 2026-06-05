<script setup>
import AppSidebar from '../components/layout/AppSidebar.vue'
</script>

<template>
  <div class="layout">
    <AppSidebar />
    <main class="layout-main">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  height: 100dvh;
  overflow: hidden;
}

.layout-main {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  background: radial-gradient(
    circle at top center,
    #0A1830 0%,
    #071426 35%,
    #02050D 100%
  );
}
</style>
