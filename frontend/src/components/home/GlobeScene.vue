<template>
  <div class="absolute inset-0 overflow-hidden">
    <div class="globe-vignette" aria-hidden="true" />
    <div class="globe-glow" aria-hidden="true" />
  </div>
</template>

<style scoped>
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