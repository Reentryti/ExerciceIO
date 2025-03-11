<template>
  <div id="app" class="">

    <!-- Barre de navigation masquée sur les pages d'authentification -->
    <nav v-if="!isAuthPage && showNavBar" class="bg-white">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">

        <div class="flex h-16 items-center justify-between">

          <div class="flex items-center">
            <!-- Logo de la plateforme -->
            <div class="shrink-0">
              <img class="size-10" src="../public/logo.png" alt="Logo">
            </div>

            <div class="hidden md:block">
              <div class="ml-10 flex items-baseline space-x-4">
                
                <router-link to="/dashboard-etudiant" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
                  Tableau de bord
                </router-link>
                <router-link to="/exercices" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
                  Exercices
                </router-link>
                <router-link to="/correction" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
                  Corrections
                </router-link>
                <router-link to="/donnees" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
                  Données
                </router-link>
                <!-- <router-link to="/profil" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
                  Profil
                </router-link> -->
              </div>
            </div>

          </div>

          <div class="">
            <div class="">

              <!-- Profile dropdown -->
              <div class="flex flex-row-reverse mt-2">
                <div class="">
                  <button @click="show = !show" type="button" class=" p-1 ">
                    <img class="size-8 rounded-full" src="../public/images/user.png" alt="">
                  </button>
                </div>
                <div class="pr-4 flex flex-col text-right text-xs md:text-sm">
                  <router-link to="/profil" class="" >
                    Mon profil
                  </router-link>
                  <a href="#" @click="logout" class="p-1 rounded-xl hover:bg-red-400 hover:text-white">
                    Se déconnnecter
                  </a>
                </div>
              </div>

            </div>
          </div>
        </div>

      </div>

    </nav>

    <!-- Contenu principal -->
    <main class="">
      <router-view></router-view>
    </main> 

  </div>
</template>

<script>
import { computed, Transition } from 'vue';
import { useRoute } from 'vue-router';



export default {
  name: 'App',
  setup() {
    
    const route = useRoute();

    // Vérifie si la page actuelle est une page d'authentification
    const isAuthPage = computed(() => ['/connexion', '/inscription', 'connexion-professeur'].includes(route.path));

    // Masque la NavBar pour certaines routes
    const showNavBar = computed(() => !['Accueil','LoginProf'].includes(route.name));
    //const showBody = computed(() => !['Accueil'].includes(routes.name));
    return { isAuthPage, showNavBar };
  },

  methods: {
    logout() {
      localStorage.removeItem('token');  // Supprimer le token
      localStorage.removeItem('role');   // Supprimer le rôle
      this.$router.push('/connexion');   // Rediriger vers la page de connexion
      console.log("Déconnexion en cours...");
    },
  },
};
</script>

<style scoped>
/* Styles globaux */
.v-enter-active,
.v-enter-active{
  transition: opacity 0.5s ease;
}
.v-enter-from,
.v-leave-to{
  opacity: 0;
}

</style>