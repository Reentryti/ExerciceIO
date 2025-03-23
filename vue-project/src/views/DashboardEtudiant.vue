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
              <p v-if="!latestExercice" class="text-gray-500 mt-2 text-sm ">
                Vous n'avez aucun exercice à remettre
              </p>
              <div v-if="latestExercice" class="mt-4">
                <div class="flex justify-between items-center mb-2">
                  <h4 class="text-sm font-semibold text-gray-900">
                    {{ latestExercice.titre }}
                  </h4>
                  <span class="px-2 py-1 text-xs font-medium rounded-full" :class="isExerciceExpired(latestExercice.date_a_soumettre)? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'">
                    {{ isExerciceExpired(latestExercice.date_a_soumettre)? 'Expired' : 'A rendre' }}
                  </span>
                </div>
                <p class="text-xs text-gray-600 mb-1">{{ formatDate(latestExercice.date_a_soumettre) }}</p>
                <p class="text-sm text-gray-500 mb-3 line-clamp-2">{{ latestExercice.description }}</p>
                <router-link :to="'/exercice/' + latestExercice.id" class="text-sm text-indigo-500 ">
                  Voir les détails
                </router-link>
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
      latestExercice:null
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
    async fetchLatestExercice(){
      try{
        const token = localStorage.getItem("token");
        if(!token){
          throw new Error("Aucun token trouvé")
        }
        console.log("Making API request...");
        const response = await axios.get("http://localhost:8000/exercices/recent/", 
          {
            headers:{
              "Authorization" : `Token ${token}`,
              "Content-Type": "application/json"
            }
          });
        console.log("API response status:", response.status);
        console.log("API response data:", response.data);
        console.log("API response type:", typeof response.data);
        
        if (response.data) {
          this.latestExercice = response.data;
          console.log("latestExercice set to:", this.latestExercice);
        } else {
          console.log("No data received from API");
        }
      }catch(error){
        console.error("Erreur lors de la récupération de l'exercice:", error);
        console.error("Error details:", error.response ? error.response.data : "No response data");
      }
    },

    formatDate(dateString){
      const date = new Date(dateString);
      return date.toLocaleDateString('fr-FR',{
        day:'numeric',
        month:'long',
        year:'numeric'
      });
    },

    isExerciceExpired(dateString){
      const submissionDate = new Date(dateString);
      const today = new Date();
      return submissionDate< today;
    }
  },
  mounted() {
    this.fetchUser(); // Récupère l'utilisateur au chargement
    this.fetchLatestExercice();
  },
};
</script>

<style scoped>
/* Styles spécifiques au dashboard */
</style>