<script setup>
import BreweryList from './components/BreweryList.vue'
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <header class="bg-slate-800 text-white py-4 px-6 shadow-md fixed top-0 w-full z-10">
      <h1 class="text-xl font-bold">Open Brewery Explorer</h1>
    </header>
    <main class="container mx-auto px-4 pt-20 pb-6 flex-grow">
      <BreweryList />
    </main>
  </div>
</template>

<style scoped>
/* Tailwind classes are used instead of these styles */
</style>
