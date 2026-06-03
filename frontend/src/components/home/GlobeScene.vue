<script setup>
import { ref } from "vue";

import { useEarthGlobe } from "../../composables/useEarthGlobe.js";

const canvasRef = ref(null);

const { ready, error } = useEarthGlobe(canvasRef);
</script>

<template>
  <div class="absolute inset-0 overflow-hidden">
    <div
      ref="canvasRef"
      class="globe-canvas absolute inset-0"
    />

    <div v-if="error" class="globe-state globe-state--error">
      <p class="max-w-[min(24rem,90vw)] text-balance">{{ error }}</p>

      <small class="max-w-[min(22rem,88vw)] text-balance">
        Ative WebGPU no Chrome/Edge ou use um navegador compatível.
      </small>
    </div>

    <div v-else-if="!ready" class="globe-state">
      Carregando globo…
    </div>

    <div class="globe-vignette" aria-hidden="true" />

    <div class="globe-glow" aria-hidden="true" />
  </div>
</template>

<style scoped>
.globe-canvas :deep(canvas) {
  display: block;
  width: 100% !important;
  height: 100% !important;
}

.globe-state {
  position: absolute;
  inset: 0;
  display: grid;
  place-content: center;
  gap: 0.5rem;
  padding: 1.5rem;
  text-align: center;
  font-size: 0.85rem;
  color: rgba(232, 234, 240, 0.5);
  background: radial-gradient(
    circle at 60% 50%,
    rgba(77, 178, 255, 0.06),
    #030508
  );
}

.globe-state--error small {
  font-size: 0.72rem;
  opacity: 0.6;
}

.globe-vignette {
  pointer-events: none;
  position: absolute;
  inset: 0;
  background:
    radial-gradient(
      ellipse 52% 52% at 74% 40%,
      transparent 12%,
      rgba(3, 5, 8, 0.45) 62%
    ),
    linear-gradient(
      to right,
      rgba(3, 5, 8, 0.75) 0%,
      rgba(3, 5, 8, 0.25) 28%,
      transparent 48%
    ),
    linear-gradient(to top, rgba(3, 5, 8, 0.88) 0%, transparent 22%);
}

.globe-glow {
  pointer-events: none;
  position: absolute;
  top: 42%;
  left: 74%;
  width: 480px;
  height: 480px;
  transform: translate(-50%, -50%);
  background: radial-gradient(
    circle,
    rgba(77, 178, 255, 0.09) 0%,
    transparent 68%
  );
}
</style>
