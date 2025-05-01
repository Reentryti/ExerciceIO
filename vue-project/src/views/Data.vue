<template>
  <div class="mx-auto">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <!-- Graphique 1 : Notes par exercice -->
      <div class="bg-white rounded-lg shadow-lg p-6">
        <canvas id="gradesChart" ref="gradesChart"></canvas>
      </div>

      <!-- Graphique 2 : Progression globale -->
      <div class="bg-white rounded-lg shadow-lg p-6">
        <canvas id="progressChart" ref="progressChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { Chart, registerables } from 'chart.js';
import axios from 'axios';

Chart.register(...registerables);

export default {
  setup() {
    const gradesChart = ref(null);
    const progressChart = ref(null);
    const loading = ref(false); // Modifié pour le débug

    const fetchData = async() => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/exercices/stats/etudiant/', {
          headers: { "Authorization": `Token ${token}` }
        });
        
        createCharts(response.data);
      } catch(error) {
        console.error('Erreur:', error);
      }
    };

    const createCharts = (data) => {
      // Destruction du canvas existant s'il y en a un
      if (gradesChart.value?.chart) {
        gradesChart.value.chart.destroy();
      }
      if (progressChart.value?.chart) {
        progressChart.value.chart.destroy();
      }

      // Graphique des notes
      const gradesCtx = document.getElementById('gradesChart').getContext('2d');
      gradesChart.value = new Chart(gradesCtx, {
        type: 'bar',
        data: {
          labels: data.exercices,
          datasets: [{
            label: 'Notes',
            data: data.notes,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 20,
              title: { display: true, text: 'Note /20' }
            }
          }
        }
      });

      // Graphique de progression
      const progressCtx = document.getElementById('progressChart').getContext('2d');
      progressChart.value = new Chart(progressCtx, {
        type: 'line',
        data: {
          labels: data.exercices,
          datasets: [{
            label: 'Moyenne cumulative',
            data: data.progression,
            fill: true,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 2,
            tension: 0.1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 20,
              title: { display: true, text: 'Moyenne /20' }
            }
          }
        }
      });
    };

    onMounted(() => {
      fetchData();
    });

    return {
      gradesChart,
      progressChart,
      loading
    };
  }
};
</script>

<style scoped>
canvas {
  width: 100% !important;
  min-height: 300px;
}
</style>