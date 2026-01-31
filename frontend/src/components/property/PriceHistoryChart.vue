<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  TimeScale,
  Title,
  Tooltip,
  Legend,
  Filler,
  CategoryScale
} from 'chart.js';

// Register Chart.js components
Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  TimeScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend,
  Filler
);

interface PriceHistory {
  date: string;
  price: number;
}

interface Props {
  history: PriceHistory[];
}

const props = defineProps<Props>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const formatPrice = (value: number) => {
  if (value >= 1000000) {
    return `$${(value / 1000000).toFixed(2)}M`;
  }
  return `$${(value / 1000).toFixed(0)}K`;
};

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short',
    day: 'numeric'
  });
};

const createChart = () => {
  if (!chartCanvas.value || !props.history.length) return;

  // Destroy existing chart
  if (chartInstance) {
    chartInstance.destroy();
  }

  // Sort history by date
  const sortedHistory = [...props.history].sort((a, b) => 
    new Date(a.date).getTime() - new Date(b.date).getTime()
  );

  const labels = sortedHistory.map(h => formatDate(h.date));
  const data = sortedHistory.map(h => h.price);

  chartInstance = new Chart(chartCanvas.value, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Property Value',
        data,
        borderColor: '#D4AF37',
        backgroundColor: (context) => {
          const ctx = context.chart.ctx;
          const gradient = ctx.createLinearGradient(0, 0, 0, 300);
          gradient.addColorStop(0, 'rgba(212, 175, 55, 0.3)');
          gradient.addColorStop(1, 'rgba(212, 175, 55, 0)');
          return gradient;
        },
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 6,
        pointHoverRadius: 8,
        pointBackgroundColor: '#D4AF37',
        pointBorderColor: '#000',
        pointBorderWidth: 2,
        pointHoverBackgroundColor: '#D4AF37',
        pointHoverBorderColor: '#000',
        pointHoverBorderWidth: 3,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(20, 20, 20, 0.95)',
          titleColor: '#D4AF37',
          bodyColor: '#fff',
          borderColor: '#D4AF37',
          borderWidth: 1,
          padding: 12,
          displayColors: false,
          callbacks: {
            label: (context) => {
              return `Value: ${formatPrice(context.parsed.y)}`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: {
            display: false,
            drawBorder: false
          },
          ticks: {
            color: '#9ca3af',
            font: {
              size: 11
            }
          }
        },
        y: {
          grid: {
            color: 'rgba(255, 255, 255, 0.05)',
            drawBorder: false
          },
          ticks: {
            color: '#9ca3af',
            font: {
              size: 11
            },
            callback: (value) => formatPrice(Number(value))
          }
        }
      }
    }
  });
};

onMounted(() => {
  createChart();
});

watch(() => props.history, () => {
  createChart();
}, { deep: true });
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 300px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
}

canvas {
  max-height: 100%;
}
</style>