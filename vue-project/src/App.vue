<template>
  <div id="app" class="">
    <!-- Barre de navigation -->
    <nav v-if="!isAuthPage && showNavBar" class="bg-white">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="flex h-16 items-center justify-between">
          <div class="flex items-center">
            <!-- Logo -->
            <div class="shrink-0">
              <img class="size-10" src="../public/logo.png" alt="Logo">
            </div>

            <!-- Liens en fonction du rôle -->
            <div class="hidden md:block">
              <div class="ml-10 flex items-baseline space-x-4">
                <!-- Menu Étudiant -->
                <template v-if="userRole === 'etudiant'">
                  <router-link to="/dashboard-etudiant" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
                    Tableau de bord
                  </router-link>
                  <router-link to="/exercices" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
                    Exercices
                  </router-link>
                  <router-link to="/correction" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
                    Corrections
                  </router-link>
                </template>

                <!-- Menu Professeur -->
                <template v-else-if="userRole === 'professeur'">
                  <router-link to="/dashboard-professeur" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
                    Tableau de bord
                  </router-link>
                  <router-link to="/gerer-exercices" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
                    Gérer les exercices
                  </router-link>
                  <router-link to="/corrections" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
                    Corriger copies
                  </router-link>
                </template>
              </div>
            </div>
          </div>

          <!-- Menu utilisateur -->
          <div class="flex items-center">
            <div class="flex flex-row-reverse mt-2">
              <div>
                <button @click="show = !show" type="button" class="p-1">
                  <img class="size-8 rounded-full" src="../public/images/user.png" alt="">
                </button>
              </div>
              <div class="pr-4 flex flex-col text-right text-xs md:text-sm">
                <router-link to="/profil" class="">
                  Mon profil
                </router-link>
                <a href="#" @click="logout" class="p-1 rounded-xl hover:bg-red-400 hover:text-white">
                  Se déconnecter
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <main class="">
      <router-view></router-view>
    </main> 
  </div>
</template>

<script>
import { computed, ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

export default {
  name: 'App',
  setup() {
    const route = useRoute();
    const userRole = ref(null);

    // Récupérer le rôle au montage du composant
    onMounted(() => {
      userRole.value = localStorage.getItem('role');
    });

    const isAuthPage = computed(() => 
      ['/connexion', '/inscription', '/connexion-professeur'].includes(route.path)
    );

    const showNavBar = computed(() => 
      !['Accueil', 'LoginProf'].includes(route.name) && userRole.value
    );

    return { isAuthPage, showNavBar, userRole };
  },

  methods: {
    // Fonction de déconnextion
    logout() {
      const role = localStorage.getItem('role');
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      // Redirection selon le role
      if (role === 'professeur') {
        this.$router.push('/connexion-professeur');
      } else {
        this.$router.push('/connexion');
      }
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