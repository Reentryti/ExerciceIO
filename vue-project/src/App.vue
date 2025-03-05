<template>
  <div id="app" class="bg-center bg-cover min-h-screen"style="background-image: url('../public/images/background_register1.jpg');">

    <!-- NavBar -->
    <nav v-if="!isAuthPage" class="bg-white shadow-lg">
      <div class="container mx-auto px-6 py-4 flex justify-between items-center">
        <div class="text-2xl font-bold text-gray-800">
          Plateforme SGBD
        </div>
        <div class="flex space-x-4">
          <router-link to="/" class="text-gray-700 hover:text-blue-500" active-class="text-blue-500">
            Accueil
          </router-link>
          <router-link to="/dashboard-etudiant" class="text-gray-700 hover:text-blue-500" active-class="text-blue-500">
            Tableau de bord
          </router-link>
          <router-link to="/exercices" class="text-gray-700 hover:text-blue-500" active-class="text-blue-500">
            Exercices
          </router-link>
          <router-link to="/corrections" class="text-gray-700 hover:text-blue-500" active-class="text-blue-500">
            Corrections
          </router-link>
          <router-link to="/donnees" class="text-gray-700 hover:text-blue-500" active-class="text-blue-500">
            Données
          </router-link>
          <router-link to="/profil" class="text-gray-700 hover:text-blue-500" active-class="text-blue-500">
            Profil
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Contenu principal -->
    <main class="container mx-auto px-6 py-8">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

export default {
  name: 'App',
  setup() {
    const route = useRoute();
    const isAuthPage = computed(() => ['/connexion', '/inscription'].includes(route.path));

    return { isAuthPage };
  },
};
</script>

<style>
/* Styles globaux */
</style>