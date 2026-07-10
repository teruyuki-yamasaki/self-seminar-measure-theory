<template>
  <aside class="example-box">
    <p v-if="title" class="example-box-title">{{ title }}</p>
    <div class="example-box-content">
      <slot />
    </div>
  </aside>
</template>

<script setup lang="ts">
defineProps<{
  title?: string;
}>();
</script>

<style scoped>
.example-box {
  margin: 0.9rem 0;
  border: 1px solid var(--measure-border);
  border-radius: 0.6rem;
  background: var(--measure-panel);
  color: var(--measure-text);
  padding: 0.8rem 1rem;
  font-size: 0.82rem;
  line-height: 1.5;
  box-shadow: var(--measure-shadow-soft);
}

.example-box-title {
  margin: 0 0 0.45rem;
  color: var(--measure-accent);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.04em;
}

:deep(p) {
  margin: 0.2rem 0;
}

:deep(.katex-display) {
  margin: 0.35rem 0;
}

:deep(.katex) {
  font-size: 0.95em;
}
</style>
