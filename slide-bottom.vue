<template>
  <div class="measure-page-number" aria-label="page number">
    {{ $slidev.nav.currentPage }} / {{ $slidev.nav.total }}
  </div>
</template>

<style scoped>
.measure-page-number {
  position: absolute;
  right: 1.35rem;
  bottom: 1rem;
  z-index: 20;
  color: var(--measure-muted);
  font-size: 0.72rem;
  font-variant-numeric: tabular-nums;
  letter-spacing: 0;
  line-height: 1;
  opacity: 0.78;
  pointer-events: none;
}
</style>
