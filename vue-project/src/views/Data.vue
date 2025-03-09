<template>
    <div class="min-h-screen bg-gray-100 p-8">
      <div class="max-w-7xl mx-auto">
        <!-- Titre de la page -->
        <h1 class="text-3xl font-bold text-gray-800 mb-8">Mes Performances</h1>
  
        <!-- Grille pour les graphiques -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Graphique 1 : Notes par exercice -->
          <div class="bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-xl font-semibold text-gray-700 mb-4">Notes par exercice</h2>
            <canvas ref="gradesChart"></canvas>
          </div>
  
          <!-- Graphique 2 : Progression globale -->
          <div class="bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-xl font-semibold text-gray-700 mb-4">Progression globale</h2>
            <canvas ref="progressChart"></canvas>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { Chart, registerables } from 'chart.js';
  
  // Enregistrer les composants nécessaires de Chart.js
  Chart.register(...registerables);
  
  export default {
    setup() {
      const gradesChart = ref(null);
      const progressChart = ref(null);
  
      onMounted(() => {
        // Données pour le graphique des notes par exercice
        const gradesData = {
          labels: ['Exercice 1', 'Exercice 2', 'Exercice 3', 'Exercice 4', 'Exercice 5'],
          datasets: [
            {
              label: 'Notes',
              data: [12, 15, 14, 10, 18],
              backgroundColor: 'rgba(79, 70, 229, 0.2)',
              borderColor: 'rgba(79, 70, 229, 1)',
              borderWidth: 1,
            },
          ],
        };
  
        // Options pour le graphique des notes
        const gradesOptions = {
          scales: {
            y: {
              beginAtZero: true,
              max: 20,
            },
          },
        };
  
        // Créer le graphique des notes
        new Chart(gradesChart.value, {
          type: 'bar',
          data: gradesData,
          options: gradesOptions,
        });
  
        // Données pour le graphique de progression globale
        const progressData = {
          labels: ['Semaine 1', 'Semaine 2', 'Semaine 3', 'Semaine 4'],
          datasets: [
            {
              label: 'Progression',
              data: [30, 50, 70, 90],
              fill: true,
              backgroundColor: 'rgba(79, 70, 229, 0.2)',
              borderColor: 'rgba(79, 70, 229, 1)',
              borderWidth: 2,
            },
          ],
        };
  
        // Options pour le graphique de progression
        const progressOptions = {
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
            },
          },
        };
  
        // Créer le graphique de progression
        new Chart(progressChart.value, {
          type: 'line',
          data: progressData,
          options: progressOptions,
        });
      });
  
      return {
        gradesChart,
        progressChart,
      };
    },
  };
  </script>
  
  <style scoped>
  /* Styles spécifiques à cette vue */
  </style>