<template>
  <div class="min-h-screen">
    <!-- Contenu principal -->
    <main>
      <div class="bg-white flex flex-wrap w-full">

        <!-- Bloc de bienvenue -->
        <div class="mx-auto max-w-md h-96 overflow-hidden rounded-xl bg-white shadow-md md:max-w-2xl">
          <div class="md:flex ">
            <div class="md:shrink-0 ">
              <img class="h-48 w-full object-cover md:h-96 md:w-96" src="../../public/images/bdd.jpg" alt="BackgroundImage"/>
            </div>
            <div class="p-8">
              <div class="text-sm font-semibold tracking-wide text-indigo-500 uppercase">
                {{ currentDate }}
              </div>
              <div class="mt-1 block text-4xl leading-tight font-medium text-black">
                Bon retour, 
                <span class="relative inline-block before:absolute before:-inset-1 before:block before:-skew-y-3 before:bg-red-400">
                <span class="relative text-white">
                  {{ user ? user.prenom : "Eleve" }}! 
                </span>
              </span>
              Des exercices à faire ?
              </div>
            </div>
          </div>
        </div>

        <!-- Bloc d'activités -->
        <div class="grid md:grid-cols-3 grid-cols-1 gap-8 w-full md:w-full h-full md:h-full mt-10 mb-20 px-6 md:px-20 ">

          <!-- Sous-bloc exercices -->
          <div class="flex col-span-1 h-96 bg-white rounded-lg px-6 py-8 ring shadow-xl ring-gray-900/5">
            <div>
              <h3 class="text-gray-900 mt-5 text-base font-bold tracking-tight">
                Exercices à rendre
              </h3>
              <p class="text-gray-500 mt-2 text-sm ">
                Vous n'avez aucun exercice à remettre
              </p>
              <div class="border w-full">
                <ul role="list" class="divide-y divide-gray-100">
                  <li v-for="person in people" :key="person.email" class="flex justify-between gap-x-6 py-5">
                    <div class="flex min-w-0 gap-x-4">
                      <div class="min-w-0 flex-auto">
                        <p class="text-sm/6 font-semibold text-gray-900">{{ person.name }}</p>
                        <p class="mt-1 truncate text-xs/5 text-gray-500">{{ person.email }}</p>
                      </div>
                    </div>
                    <div class="hidden shrink-0 sm:flex sm:flex-col sm:items-end">
                      <p class="text-sm/6 text-gray-900">{{ person.role }}</p>
                      <p v-if="person.lastSeen" class="mt-1 text-xs/5 text-gray-500">
                        Last seen <time :datetime="person.lastSeenDateTime">{{ person.lastSeen }}</time>
                      </p>
                      <div v-else class="mt-1 flex items-center gap-x-1.5">
                        <div class="flex-none rounded-full bg-emerald-500/20 p-1">
                          <div class="size-1.5 rounded-full bg-emerald-500" />
                        </div>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          
          <!-- Sous-bloc notes -->
          <div class="col-span-2 bg-white rounded-lg px-6 py-8 ring shadow-xl ring-gray-900/5">
            <div>
              <h3 class="text-gray-900 mt-5 text-base font-bold tracking-tight">
                Statistiques
              </h3>
              <div class="mt-2">
                <Data />
              </div>
            </div>
          </div>
          
         
          <!-- Sous-bloc classes -->
          <div class="col-span-2 bg-white rounded-lg px-6 py-8 ring shadow-xl ring-gray-900/5">
            <div>
              <h3 class="text-gray-900 mt-5 text-base font-bold tracking-tight">
                Ressources
              </h3>
              <p class="text-gray-500 mt-2 text-sm">
                Vous n'avez aucun exercice à remettre
              </p>
            </div>
          </div>


          <!-- Sous-bloc ressources -->
          <div class="col-span-1 bg-white rounded-lg px-6 py-8 ring shadow-xl ring-gray-900/5 text-center ">
            <div class="items-center justify-items-center">
              <h3 class="text-gray-900 mt-5 text-base font-bold tracking-tight">
                Moyenne de la classe
              </h3>
              <div class="bg-red-400 rounded-full size-30 text-center flex items-center justify-center mt-3">
                <p class="text-white text-5xl font-extrabold">
                  13/20
                </p>
              </div>
              <p class="text-gray-500 mt-2 text-sm">
                Vous n'avez aucun exercice à remettre
              </p>
            </div>
          </div>

        </div>

        <!-- Bloc de ressources-->
        <!-- <div class="mt-20 mx-auto max-w-md h-64 overflow-hidden rounded-xl bg-white shadow-md md:max-w-full text-align-left px-8 py-8">
          <div class="">
            <p class="text-4xl">Cours & Révisions</p>
            <p class="text-gray-500 text-xl mt-5 text-justify">Envie d'approfondir tes connaissances en matière de bases de données ? Apprends tes cours et accéde à un large éventail de documents</p>
          </div>
          <div class="mt-8 underline">
            <a href="">Suivre ce lien pour accéder aux cours ></a>
          </div>
        </div> -->

    </div>
 </main>
 
  </div>
</template>

<script>
import axios from 'axios';
import Data from "./Data.vue"

export default {
  name: 'Dashboard',
  components:{
    Data
  },
  data(){
    return {
      user:null, 
      currentDate:"",
    };
  },

  methods: {
    async fetchUser() {
      try {
        const token = localStorage.getItem("token"); // Récupérer le token

        if (!token) {
          throw new Error("Aucun token trouvé, l'utilisateur n'est pas connecté.");
        }

        const response = await axios.get("http://localhost:8000/api/user/", {
          headers: {
            "Authorization": `Token ${token}`, 
            "Content-Type": "application/json"
          }
        });

        this.user = response.data.user;
        this.currentDate = response.data.date;
      } catch (error) {
        console.error("Erreur lors de la récupération de l'utilisateur :", error);
      }
    },
  },
  mounted() {
    this.fetchUser(); // Récupère l'utilisateur au chargement
  },
};
</script>

<style scoped>
/* Styles spécifiques au dashboard */
</style>