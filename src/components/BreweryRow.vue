<template>
  <tr class="hover:bg-gray-50 border-t border-gray-200">
    <td class="py-3 px-4">{{ brewery.name }}</td>
    <td class="py-3 px-4">{{ brewery.brewery_type }}</td>
    <td class="py-3 px-4">{{ brewery.city }}</td>
    <td class="py-3 px-4">{{ brewery.state }}</td>
    <td class="py-3 px-4">
      <a
        v-if="brewery.website_url"
        :href="brewery.website_url"
        target="_blank"
        rel="noopener"
        class="text-blue-600 hover:underline"
      >
        {{ brewery.website_url }}
      </a>
      <span v-else class="text-gray-500">N/A</span>
    </td>
  </tr>
</template>

<script setup lang="ts">
  import { Brewery } from "../types/brewery";

  defineProps<{ brewery: Brewery }>();
</script>

<style scoped></style>
