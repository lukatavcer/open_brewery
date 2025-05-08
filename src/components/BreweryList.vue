<script setup>
import { ref, onMounted } from 'vue';

// State to store the brewery data
const breweries = ref([]);
const loading = ref(true);
const error = ref(null);

// Function to fetch breweries from the API
const fetchBreweries = async () => {
  try {
    loading.value = true;
    const response = await fetch('https://api.openbrewerydb.org/v1/breweries');

    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }

    const data = await response.json();
    breweries.value = data;
  } catch (err) {
    error.value = err.message || 'Failed to fetch breweries';
    console.error('Error fetching breweries:', err);
  } finally {
    loading.value = false;
  }
};

// Fetch breweries when the component is mounted
onMounted(fetchBreweries);
</script>

<template>
  <div class="my-8">
    <h2 class="text-2xl font-semibold mb-4 text-gray-800">Brewery List</h2>

    <div v-if="loading" class="p-4 text-center">
      Loading breweries...
    </div>

    <div v-else-if="error" class="p-4 text-center text-red-600">
      {{ error }}
    </div>

    <div v-else-if="breweries.length === 0" class="p-4 text-center">
      No breweries found.
    </div>

    <div v-else class="mt-4 overflow-x-auto">
      <table class="min-w-full bg-white border border-gray-200 rounded-lg overflow-hidden">
        <thead class="bg-gray-100">
          <tr>
            <th class="py-3 px-4 text-left font-semibold text-gray-700">Name</th>
            <th class="py-3 px-4 text-left font-semibold text-gray-700">Type</th>
            <th class="py-3 px-4 text-left font-semibold text-gray-700">City</th>
            <th class="py-3 px-4 text-left font-semibold text-gray-700">State</th>
            <th class="py-3 px-4 text-left font-semibold text-gray-700">Website</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="brewery in breweries" :key="brewery.id" class="hover:bg-gray-50 border-t border-gray-200">
            <td class="py-3 px-4">{{ brewery.name }}</td>
            <td class="py-3 px-4">{{ brewery.brewery_type }}</td>
            <td class="py-3 px-4">{{ brewery.city }}</td>
            <td class="py-3 px-4">{{ brewery.state }}</td>
            <td class="py-3 px-4">
              <a v-if="brewery.website_url" :href="brewery.website_url" target="_blank" rel="noopener" class="text-blue-600 hover:underline">
                Visit Website
              </a>
              <span v-else class="text-gray-500">N/A</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
/* Tailwind classes are used instead of these styles */
</style>
