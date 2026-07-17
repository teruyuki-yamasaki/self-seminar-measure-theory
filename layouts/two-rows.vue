<template>
  <div class="slidev-layout two-rows">
    <div class="two-rows-main">
      <slot />
    </div>
    <div class="two-rows-figure">
      <slot name="right" />
      <slot name="figure" />
    </div>
  </div>
</template>
