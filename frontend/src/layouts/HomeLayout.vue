<script setup>
import AppNav from '../components/layout/AppNav.vue'
</script>

<template>
  <div class="home-layout">
    <!-- <AppNav /> -->
    <router-view />
  </div>
</template>

<style scoped>
.home-layout {
  width: 100%;
  height: 100vh;
  height: 100dvh;
  overflow: hidden;
  background-color: #030508;
}
</style>
