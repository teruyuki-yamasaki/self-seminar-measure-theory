<template>
  <aside class="seminar-note">
    <slot />
  </aside>
</template>

<style scoped>
.seminar-note {
  margin: 1.2rem 0;
  border-left: 4px solid var(--seminar-accent);
  border-radius: 0.55rem;
  background: var(--seminar-note-bg);
  color: var(--seminar-text);
  padding: 0.8rem 1rem;
  font-size: 0.9rem;
  line-height: 1.65;
}

:deep(p) {
  margin: 0;
}
</style>
