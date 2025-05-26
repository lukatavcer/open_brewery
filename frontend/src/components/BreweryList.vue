<template>
  <div class="my-8">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-semibold text-gray-800">Brewery List</h2>

      <!-- Backend toggle switch -->
      <div class="flex items-center space-x-2">
        <span class="text-sm text-gray-600">API Source:</span>
        <button 
          @click="toggleBackend" 
          class="px-3 py-1 text-sm rounded-md"
          :class="useBackend ? 'bg-green-500 text-white' : 'bg-blue-500 text-white'"
        >
          {{ useBackend ? 'Django Backend' : 'Open Brewery API' }}
        </button>
      </div>
    </div>

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
        <div class="flex-1">
          <label for="type-filter" class="block text-sm font-medium text-gray-700 mb-1">
            Group by
          </label>
          <select
            id="group-by"
            v-model="groupBy"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option :value="undefined">--</option>
            <option v-for="option in groupByOptions" :key="option" :value="option">
              {{ formatFieldName(option) }}
            </option>
          </select>
        </div>
        <div class="flex items-end space-x-2">
          <button
            @click="resetFilters"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500"
          >
            Reset Filters
          </button>
          <button
            v-if="useBackend"
            @click="syncWithBackend"
            class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            :disabled="syncing"
          >
            {{ syncing ? 'Syncing...' : 'Sync with Backend' }}
          </button>
        </div>
      </div>
      <!-- Results count -->
      <div class="mb-4 text-sm text-gray-600">
        Showing {{ filteredBreweries.length }} of {{ allBreweries.length }}
        {{ pluralizeBrewery(allBreweries.length) }}
      </div>

      <!-- Chart visualization -->
      <div v-if="groupBy" class="mb-6">
        <div class="flex items-center justify-between mb-2">
          <h3 class="text-lg font-medium text-gray-700">Data Visualization</h3>
          <div class="flex space-x-2">
            <button
              @click="chartType = 'bar'"
              class="px-3 py-1 text-sm rounded-md"
              :class="
                chartType === 'bar'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              "
            >
              Bar Chart
            </button>
            <button
              @click="chartType = 'pie'"
              class="px-3 py-1 text-sm rounded-md"
              :class="
                chartType === 'pie'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              "
            >
              Pie Chart
            </button>
          </div>
        </div>
        <BreweryChart
          :grouped-data="groupedBreweries"
          :group-by="groupBy"
          :chart-type="chartType"
        />
      </div>

      <!-- Breweries table -->
      <div class="mt-4 overflow-x-auto">
        <table class="min-w-full bg-white border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-100">
            <tr>
              <th
                class="py-3 px-4 text-left font-semibold text-gray-700"
                v-for="(header, index) in tableHeaders"
                :key="index"
              >
                {{ header }}
              </th>
            </tr>
          </thead>
          <tbody>
            <template v-if="groupBy">
              <template v-for="[group, breweriesList] in Object.entries(groupedBreweries)">
                <tr class="bg-gray-200">
                  <td :colspan="tableHeaders.length" class="py-2 px-4 font-bold text-gray-800">
                    {{ formatFieldName(groupBy) }}: {{ group }} ({{ breweriesList.length
                    }}{{ pluralizeBrewery(breweriesList.length) }})
                  </td>
                </tr>
                <BreweryRow
                  v-for="brewery in breweriesList"
                  :key="brewery.id"
                  :brewery="brewery"
                ></BreweryRow>
              </template>
            </template>
            <template v-else>
              <BreweryRow
                v-for="brewery in filteredBreweries"
                :key="brewery.id"
                :brewery="brewery"
              ></BreweryRow>
            </template>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { computed, onMounted, ref, watch } from "vue";
  import BreweryRow from "./BreweryRow.vue";
  import BreweryChart from "./BreweryChart.vue";
  import { Brewery } from "../types/brewery";
  import { fetchBreweries, syncBreweriesWithBackend, API_CONFIG } from "../api/breweryService";

  // Use the API_CONFIG to determine if we're using the backend
  const useBackend = ref<boolean>(API_CONFIG.USE_DJANGO_BACKEND);
  const syncing = ref<boolean>(false);

  // Watch for changes to API_CONFIG.USE_DJANGO_BACKEND
  watch(() => API_CONFIG.USE_DJANGO_BACKEND, (newValue) => {
    useBackend.value = newValue;
    // Reload breweries when switching backends
    loadBreweries();
  });

  // State to store the brewery data
  const allBreweries = ref<Brewery[]>([]);
  const loading = ref<boolean>(true);
  const error = ref<string | null>(null);
  const tableHeaders = ["Name", "Type", "City", "State", "Country", "Phone", "Website"];

  // Function to convert field names to user-friendly labels
  const formatFieldName = (fieldName: string): string => {
    return fieldName
      .split("_")
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  // Filtering state
  const groupByOptions: (keyof Brewery)[] = ["brewery_type", "city", "state", "country"];
  const groupBy = ref<keyof Brewery | undefined>(undefined);
  const nameFilter = ref<string>("");
  const typeFilter = ref<string>("all");

  // Chart state
  const chartType = ref<"bar" | "pie">("bar");

  // Get unique brewery types for the dropdown
  const breweryTypes = computed(() => {
    const types = new Set(allBreweries.value.map(brewery => brewery.brewery_type));
    return Array.from(types).sort();
  });

  // Apply filters to breweries
  const filteredBreweries = computed(() => {
    return allBreweries.value.filter(brewery => {
      // Filter by name (case-insensitive)
      const nameMatch = brewery.name.toLowerCase().includes(nameFilter.value.toLowerCase());

      // Filter by type
      const typeMatch = typeFilter.value === "all" || brewery.brewery_type === typeFilter.value;

      return nameMatch && typeMatch;
    });
  });

  // Grouping: Group items by a relevant attribute (e.g., brewery type, etc.) and display grouped totals or subtotals.
  const groupedBreweries = computed(() => {
    if (!groupBy.value) return {};

    return filteredBreweries.value.reduce((groups: Record<string, Brewery[]>, brewery) => {
      const key = String(brewery[groupBy.value as keyof Brewery] ?? "Unknown");
      if (!groups[key]) {
        groups[key] = [];
      }
      groups[key].push(brewery);
      return groups;
    }, {});
  });

  // Reset filters
  const resetFilters = () => {
    nameFilter.value = "";
    typeFilter.value = "all";
  };

  const pluralizeBrewery = (count: number): string => {
    return count === 1 ? "brewery" : "breweries";
  };

  // Load breweries data using the API service
  const loadBreweries = async () => {
    try {
      loading.value = true;
      allBreweries.value = await fetchBreweries();
    } catch (err: any) {
      error.value = err.message || "Failed to fetch breweries";
    } finally {
      loading.value = false;
    }
  };

  // Function to toggle between backends
  const toggleBackend = () => {
    // Toggle the API_CONFIG setting
    API_CONFIG.USE_DJANGO_BACKEND = !API_CONFIG.USE_DJANGO_BACKEND;
    // useBackend will be updated by the watcher
  };

  // Function to sync breweries with the backend
  const syncWithBackend = async () => {
    if (!useBackend.value) return;

    try {
      syncing.value = true;
      const result = await syncBreweriesWithBackend();
      console.log(result.message);

      // Reload breweries after syncing
      await loadBreweries();
    } catch (err: any) {
      error.value = err.message || "Failed to sync breweries";
    } finally {
      syncing.value = false;
    }
  };

  // Fetch breweries when the component is mounted
  onMounted(loadBreweries);
</script>

<style scoped></style>
