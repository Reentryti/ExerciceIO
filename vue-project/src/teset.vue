<template>
    <div id="app" class="bg-center bg-repeat-round min-h-screen">
      <!-- NavBar (masquée sur les pages d'authentification) -->
      <nav v-if="!isAuthPage && showNavBar" class="bg-inherit shadow-lg flex justify-between items-center flex-wrap p-2 px-6">
        <div class="container mx-auto px-6 py-4 flex justify-between items-center">
          <div class="text-2xl font-bold text-white">
            Plateforme SGBD
          </div>
          <div class="block md:hidden">
            <label id="nav-toggle" for="toggleNavbar" class="flex gap-1 p-2 px-4 border border-current rounded-lg cursor-pointer select-none text-black">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 " fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7">
                </path>
              </svg>
            </label>
          </div>
  
          <ul class="text-xl md:text-lg my-5 md:my-0 h-0 w-full md:w-auto md:h-fit overflow-hidden peer-checked:h-fit absolute md:relative peer-checked:relative flex gap-3 items-center md:justify-center md:peer-checked:items-center justify-stretch peer-checked:flex-grow peer-checked:flex-col md:peer-checked:flex-row md:peer-checked:flex-grow-0  opacity-0 md:opacity-100 peer-checked:opacity-100 transition duration-300 peer-checked:translate-y-2 md:peer-checked:translate-y-0">
            <li class="py-2 px-4 text-center">
              <router-link to="/dashboard-etudiant" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
                Tableau de bord
              </router-link>
            </li>
            <li class="py-2 px-4 text-center">
              <router-link to="/exercices" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
                Exercices
              </router-link>
            </li>
            <li class="py-2 px-4 text-center">
              <router-link to="/donnees" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
                Données
              </router-link>
            </li>
            <li class="py-2 px-4 text-center">
              <router-link to="/profil" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
                Profil
              </router-link>
            </li>
          </ul>
  
          <input type="checkbox" name="" id="toggleNavbar" class="peer hidden">
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
  
      // Vérifie si la page actuelle est une page d'authentification
      const isAuthPage = computed(() => ['/connexion', '/inscription', 'connexion-professeur'].includes(route.path));
  
      // Masque la NavBar pour certaines routes
      const showNavBar = computed(() => !['Accueil'].includes(route.name));
      //const showBody = computed(() => !['Accueil'].includes(routes.name));
      return { isAuthPage, showNavBar };
    },
  };
  </script>
  
  <style>
  /* Styles globaux */
  
  </style>