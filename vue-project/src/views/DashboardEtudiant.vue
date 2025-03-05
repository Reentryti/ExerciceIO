<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Barre latérale -->
    <aside class="fixed inset-y-0 left-0 w-64 bg-white shadow-lg">
      <div class="p-6">
        <h2 class="text-2xl font-bold text-gray-800">Plateforme SGBD</h2>
      </div>
      <nav class="mt-6">
        <router-link
          to="/dashboard"
          class="block px-6 py-2 text-gray-700 hover:bg-gray-200"
        >
          Tableau de bord
        </router-link>
        <router-link
          to="/exercices"
          class="block px-6 py-2 text-gray-700 hover:bg-gray-200"
        >
          Exercices
        </router-link>
        <router-link
          to="/profil"
          class="block px-6 py-2 text-gray-700 hover:bg-gray-200"
        >
          Profil
        </router-link>
      </nav>
    </aside>

    <!-- Contenu principal -->
    <main class="ml-64 p-6">
      <!-- Barre de navigation supérieure -->
      <header class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold text-gray-800">Tableau de bord</h1>
        <div class="flex items-center space-x-4">
          <button class="p-2 text-gray-600 hover:text-gray-800">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
              />
            </svg>
          </button>
          <div class="relative">
            <img
              src="https://via.placeholder.com/40"
              alt="Profil"
              class="rounded-full cursor-pointer"
              @click="toggleDropdown"
            />
            <div
              v-if="dropdownOpen"
              class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg"
            >
              <router-link
                to="/profil"
                class="block px-4 py-2 text-gray-700 hover:bg-gray-200"
              >
                Profil
              </router-link>
              <button
                @click="deconnexion"
                class="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-200"
              >
                Déconnexion
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Statistiques -->
      <section class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold text-gray-700">Exercices soumis</h3>
          <p class="text-2xl font-bold text-blue-500">12</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold text-gray-700">Notes moyennes</h3>
          <p class="text-2xl font-bold text-green-500">15/20</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold text-gray-700">Progression</h3>
          <p class="text-2xl font-bold text-purple-500">75%</p>
        </div>
      </section>

      <!-- Dernières activités -->
      <section class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-xl font-bold text-gray-800 mb-4">Dernières activités</h2>
        <ul>
          <li class="border-b py-3">
            <p class="text-gray-700">Vous avez soumis l'exercice "Requêtes SQL".</p>
            <p class="text-sm text-gray-500">Il y a 2 heures</p>
          </li>
          <li class="border-b py-3">
            <p class="text-gray-700">Vous avez reçu une note de 18/20 pour l'exercice "Modélisation".</p>
            <p class="text-sm text-gray-500">Il y a 1 jour</p>
          </li>
          <li class="py-3">
            <p class="text-gray-700">Nouvel exercice disponible : "Optimisation de requêtes".</p>
            <p class="text-sm text-gray-500">Il y a 3 jours</p>
          </li>
        </ul>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      dropdownOpen: false,
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    deconnexion() {
      // Logique pour déconnecter l'utilisateur
      console.log('Déconnexion...');
      this.$router.push('/connexion');
    },
  },
};
</script>

<style scoped>
/* Styles spécifiques au dashboard */
</style>