<template>
  <div class="min-h-screen">
    <!-- Contenu principal -->
    <main>
      <div class="bg-white flex flex-wrap w-full">

        <!-- Bloc de bienvenue -->
        <div class="mx-auto max-w-md overflow-hidden rounded-xl bg-white shadow-md md:max-w-2xl">
          <div class="md:flex">
            <div class="md:shrink-0">
              <img class="h-48 w-full object-cover md:h-full md:w-48" src="../../public/images/dash.jpg" alt="BackgroundImage"/>
            </div>
            <div class="p-8">
              <div class="text-sm font-semibold tracking-wide text-indigo-500 uppercase">
                {{ currentDate }}
              </div>
              <div class="mt-1 block text-4xl leading-tight font-medium text-black">
                Bon retour, {{ user ? user.prenom : "Eleve" }}! Des exercices à faire ?
              </div>
            </div>
          </div>
        </div>

        <!-- Bloc d'activités -->
        <div class="grid md:grid-cols-3 grid-cols-1 gap-8 w-full h-full md:h-80 mt-10 mb-7 px-6 ">

          <!-- Sous-bloc exercices -->
          <div class="bg-white rounded-lg px-6 py-8 ring shadow-xl ring-gray-900/5">
            <div>
              <h3 class="text-gray-900 mt-5 text-base font-bold tracking-tight">
                Exercices à rendre
              </h3>
              <p class="text-gray-500 mt-2 text-sm ">
                Vous n'avez aucun exercice à remettre
              </p>
            </div>
          </div>
          
          <!-- Sous-bloc notes -->
          <div class="bg-white rounded-lg px-6 py-8 ring shadow-xl ring-gray-900/5">
            <div>
              <h3 class="text-gray-900 mt-5 text-base font-bold tracking-tight">
                Note moyenne
              </h3>
              <p class="text-gray-500 mt-2 text-sm ">
                Vous n'avez aucun exercice à remettre
              </p>
            </div>
          </div>
          
          <!-- Sous-bloc classes -->
          <div class="bg-white rounded-lg px-6 py-8 ring shadow-xl ring-gray-900/5">
            <div>
              <h3 class="text-gray-900 mt-5 text-base font-bold tracking-tight">
                Progression
              </h3>
              <p class="text-gray-500 mt-2 text-sm">
                Vous n'avez aucun exercice à remettre
              </p>
            </div>
          </div>

        </div>

        <!-- Bloc de ressources-->
        <div class="mx-auto max-w-md h-64 overflow-hidden rounded-xl bg-white shadow-md md:max-w-full text-align-left px-8 py-8">
          <div class="">
            <p class="text-4xl">Cours & Révisions</p>
            <p class="text-gray-500 text-base mt-5 text-justify">Envie d'approfondir tes connaissances en matière de bases de données ? Apprends tes cours et accéde à un large éventail de documents</p>
          </div>
          <div class="mt-8 underline">
            <a href="">Suivez ce lien pour accéder aux cours ></a>
          </div>
        </div>

    </div>
 </main>
 
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Dashboard',
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

        this.user = response.data;
        this.currentDate = response.data.date;
      } catch (error) {
        console.error("Erreur lors de la récupération de l'utilisateur :", error);
      }
    },
  },
  mounted() {
    this.fetchUser(); // Récupère l'utilisateur au chargement
  },

    //deconnexion() {
      //localStorage.removeItem('token');  // Supprimer le token
      //localStorage.removeItem('role');   // Supprimer le rôle
      //this.$router.push('/connexion');   // Rediriger vers la page de connexion
    //},
};
</script>

<style scoped>
/* Styles spécifiques au dashboard */
</style>