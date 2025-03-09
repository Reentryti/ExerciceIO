<template>
    <div class="bg-center bg-[oklch(0.129_0.042_264.695)] bg-cover min-h-screen p-8">
      <div class="max-w-7xl mx-auto">
        <!-- Titre de la classe -->
        <h1 class="text-3xl font-bold text-white mb-8">{{ classe.name }}</h1>
  
        <!-- Description de la classe -->
        <p class="text-white mb-8">{{ classe.description }}</p>
  
        <!-- Liste des exercices -->
        <div class="bg-white rounded-lg shadow-lg p-6">
          <h2 class="text-2xl font-semibold text-gray-800 mb-6">Exercices</h2>
  
          <!-- Carte pour chaque exercice -->
          <div
            v-for="exercise in classe.exercises"
            :key="exercise.id"
            class="mb-4 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors duration-300"
          >
            <h3 class="text-lg font-medium text-gray-800">{{ exercise.title }}</h3>
            <p class="text-gray-600">{{ exercise.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        // Données de la classe (à remplacer par des données dynamiques)
        classe: {
          id: 1,
          name: "Classe de Mathématiques",
          description: "Cours de mathématiques pour la terminale.",
          exercises: [
            {
              id: 1,
              title: "Exercice 1 : Algèbre",
              description: "Résolution d'équations linéaires.",
            },
            {
              id: 2,
              title: "Exercice 2 : Géométrie",
              description: "Calculs d'aires et de volumes.",
            },
          ],
        },
      };
    },
  };
  </script>
  
  <style scoped>
  /* Styles spécifiques à cette vue */
  </style>