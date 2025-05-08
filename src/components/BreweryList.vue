<template>
  <div class="my-8">
    <h2 class="text-2xl font-semibold mb-4 text-gray-800">Brewery List</h2>

    <div v-if="loading" class="p-4 text-center">Loading breweries...</div>

    <div v-else-if="error" class="p-4 text-center text-red-600">
      {{ error }}
    </div>

    <div v-else-if="allBreweries.length === 0" class="p-4 text-center">No breweries found.</div>

    <div v-else>
      <!-- Filter controls -->
      <div class="mb-6 flex flex-col md:flex-row gap-4">
        <div class="flex-1">
          <label for="name-filter" class="block text-sm font-medium text-gray-700 mb-1">
            Search by name
          </label>
          <input
            id="name-filter"
            v-model="nameFilter"
            type="text"
            placeholder="Search breweries..."
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div class="flex-1">
          <label for="type-filter" class="block text-sm font-medium text-gray-700 mb-1">
            Filter by type
          </label>
          <select
            id="type-filter"
            v-model="typeFilter"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Types</option>
            <option v-for="type in breweryTypes" :key="type" :value="type">
              {{ type }}
            </option>
          </select>
        </div>
        <div class="flex items-end">
          <button
            @click="resetFilters"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500"
          >
            Reset Filters
          </button>
        </div>
      </div>

      <!-- Results count -->
      <div class="mb-4 text-sm text-gray-600">
        Showing {{ filteredBreweries.length }} of {{ allBreweries.length }} breweries
      </div>

      <!-- Breweries table -->
      <div class="mt-4 overflow-x-auto">
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
            <tr
              v-for="brewery in filteredBreweries"
              :key="brewery.id"
              class="hover:bg-gray-50 border-t border-gray-200"
            >
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
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted, computed } from "vue";
  import { Brewery } from "../types/brewery";

  // State to store the brewery data
  const breweries = ref<Brewery[]>([]);
  const allBreweries = ref<Brewery[]>([]);
  const loading = ref<boolean>(true);
  const error = ref<string | null>(null);

  // Filtering state
  const nameFilter = ref<string>("");
  const typeFilter = ref<string>("all");

  // Get unique brewery types for the dropdown
  const breweryTypes = computed(() => {
    const types = new Set(allBreweries.value.map(brewery => brewery.brewery_type));
    return Array.from(types).sort();
  });

  // Apply filters to breweries
  const filteredBreweries = computed(() => {
    return allBreweries.value.filter(brewery => {
      // Filter by name (case insensitive)
      const nameMatch = brewery.name.toLowerCase().includes(nameFilter.value.toLowerCase());

      // Filter by type
      const typeMatch = typeFilter.value === "all" || brewery.brewery_type === typeFilter.value;

      return nameMatch && typeMatch;
    });
  });

  // Reset filters
  const resetFilters = () => {
    nameFilter.value = "";
    typeFilter.value = "all";
  };

  // Function to fetch breweries from the API
  const fetchBreweries = async () => {
    try {
      loading.value = true;
      const response = await fetch("https://api.openbrewerydb.org/v1/breweries");

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();
      allBreweries.value = data;
      breweries.value = data;
    } catch (err: any) {
      error.value = err.message || "Failed to fetch breweries";
      console.error("Error fetching breweries:", err);
    } finally {
      loading.value = false;
    }
  };

  // Fetch breweries when the component is mounted
  onMounted(fetchBreweries);
</script>

<style scoped></style>
