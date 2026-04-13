import SidebarGerente from '@/components/SidebarGerente.vue'

<template>
  <div class="flex h-screen">
    <SidebarGerente />
    <main class="flex-1 bg-gray-100 p-8">
      <h1>
        <RouterView />
      </h1>
    </main>
  </div>
</template>

<script setup lang="ts">

import SidebarGerente from '@/components/SidebarGerente.vue'

</script>
