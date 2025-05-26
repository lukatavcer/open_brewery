<template>
  <div class="chart-container">
    <h3 class="text-xl font-semibold mb-3 text-gray-700">{{ title }}</h3>
    <div class="chart-wrapper">
      <Bar v-if="chartType === 'bar'" :data="chartData" :options="chartOptions" />
      <Pie v-else-if="chartType === 'pie'" :data="chartData" :options="chartOptions" />
      <div v-else class="text-center py-8 text-gray-500">
        Select a grouping option to view chart
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { computed, defineProps } from "vue";
  import { Bar, Pie } from "vue-chartjs";
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    CategoryScale,
    LinearScale,
    BarElement,
  } from "chart.js";

  // Register Chart.js components
  ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale, BarElement);

  // Define props
  const props = defineProps({
    groupedData: {
      type: Object as () => Record<string, any[]>,
      required: true,
    },
    groupBy: {
      type: String,
      default: "",
    },
    chartType: {
      type: String,
      default: "bar",
      validator: (value: string) => ["bar", "pie"].includes(value),
    },
  });

  // Generate chart title based on groupBy
  const title = computed(() => {
    if (!props.groupBy) return "Brewery Distribution";

    return `Breweries by ${props.groupBy
      .split("_")
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ")}`;
  });

  // Generate random colors for chart segments
  const generateColors = (count: number) => {
    const colors = [];
    for (let i = 0; i < count; i++) {
      // Generate pastel colors for better visibility
      // Use the golden ratio to spread colors evenly
      const hue = (i * 137) % 360;
      colors.push(`hsla(${hue}, 70%, 60%, 0.7)`);
    }
    return colors;
  };

  // Prepare chart data
  const chartData = computed(() => {
    if (!props.groupBy || Object.keys(props.groupedData).length === 0) {
      return { labels: [], datasets: [] };
    }

    const labels = Object.keys(props.groupedData);
    const data = labels.map(label => props.groupedData[label].length);
    const backgroundColor = generateColors(labels.length);

    return {
      labels,
      datasets: [
        {
          label: `Number of Breweries`,
          data,
          backgroundColor,
        },
      ],
    };
  });

  // Chart options
  const chartOptions = computed(() => {
    return {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: props.chartType === "pie" ? ("right" as const) : ("top" as const),
        },
        tooltip: {
          callbacks: {
            label: (context: any) => {
              const label = context.label || "";
              const value = context.raw || 0;
              const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
              const percentage = Math.round((value / total) * 100);
              return `${label}: ${value} (${percentage}%)`;
            },
          },
        },
      },
    };
  });
</script>

<style scoped>
  .chart-container {
    background-color: white;
    border-radius: 0.5rem;
    padding: 1rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  .chart-wrapper {
    position: relative;
    height: 300px;
  }
</style>
