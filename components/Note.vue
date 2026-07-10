<template>
  <aside class="measure-note">
    <slot />
  </aside>
</template>

<style scoped>
.measure-note {
  margin: 1.2rem 0;
  border-left: 4px solid var(--measure-accent);
  border-radius: 0.55rem;
  background: var(--measure-note-bg);
  color: var(--measure-text);
  padding: 0.8rem 1rem;
  font-size: 0.9rem;
  line-height: 1.65;
}

:deep(p) {
  margin: 0;
}
</style>
