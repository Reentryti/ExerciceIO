<template>
  <div class="text-center">
    <h1 class="text-4xl font-bold text-gray-800 mb-4">
      Bienvenue sur la plateforme SGBD
    </h1>
    <p class="text-lg text-gray-600 mb-8">
      Une plateforme intelligente pour l'évaluation automatisée des exercices de bases de données.
    </p>
    <div class="space-x-4">
      <router-link to="/connexion" class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600">
        Se connecter
      </router-link>
      <router-link to="/inscription" class="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600">
        S'inscrire
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Accueil',
};
</script>

<style scoped>
/* Styles spécifiques à la page d'accueil */
</style>