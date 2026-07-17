<script setup lang="ts">
import { useSlideContext } from '@slidev/client'
import { computed } from 'vue'

const { $nav, $page } = useSlideContext()

const currentPage = computed(() => $page.value)
const totalPages = computed(() => $nav.value.total.value)
</script>

<template>
  <div class="measure-page-number" aria-label="page number">
    {{ currentPage }} / {{ totalPages }}
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
