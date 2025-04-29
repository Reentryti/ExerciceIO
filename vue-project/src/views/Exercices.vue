<template>
  <!-- Bloc de bienvenue -->
  <div class="bg-gradient-to-b from-white via-white to-red-100 h-72 mx-w-md overflow-hidden mx-5 md:mx-20 mb-7">
    <div class="text-left mx-auto pl-20">
      <div>
        <p class="text-black tracking-wide text-6xl md:text-5xl font-bold text-gray-800 mb-10 mt-auto">
          Exercices
        </p>
      </div>
    </div>
  </div>

  <!-- Bloc des exercices -->
  <div class=" flex flex-col gap-10 md:flex-row-reverse mx-5 md:mx-20">
    
    <!-- Sous-bloc des exercices -->
    <div class="grid grid-col-1 w-full border border-gray-300 rounded-lg md:w-2/3">
      <div v-if="loading" class="p-8 text-center"> 
        <p>
          Chargement des exercices ...
        </p>
      </div>  
      <div v-if="error" class="p-8 text-red-500">
        {{ error }}
      </div>
      
      <!-- Item Exercice -->
      <div v-for="exercice in exercices" :key="exercice.id" class="flex flex-row ">
        <div class="flex flex-col gap-2 p-8 sm:flex-row sm:items-center sm:gap-6 sm:py-4 ...">
          <div class="space-y-2 text-center sm:text-left">
            <div class="space-y-0.5">
              <p class="text-lg font-semibold text-black">
                {{ exercice.titre }} 
              </p>
              <p class="font-medium text-gray-500">
                {{ exercice.description }}
              </p>
              <div class="flex items-center mt-2 text-sm text-gray-500">
                <span>Date limite de dépôt: {{ formatDate(exercice.date_a_soumettre) }}</span>
              </div>
            </div>
            <div class="flex gap-2 mt-4">
             <button v-if="exercice.fichier" @click="telechargerFichier(exercice.fichier)" class="px-4 py-2 border border-purple-200 text-red-400 hover:border-transparent hover:bg-gray-400 hover:text-white active:bg-purple-700 rounded-md">
              Télécharger l'exercice
             </button>
              <span v-else class="">
                Fichier non disponible
              </span>
              
              <router-link :to="`/exercice/${exercice.id}/`" class="px-4 py-2 bg-red-300 text-white hover:bg-red-400 rounded-md">
                Soumettre l'exercice
              </router-link>
            </div>
          </div>
        </div>
      </div>

    </div>


    <div></div>

     <!-- Sous-bloc des corrigés -->
    <div class="hidden md:inline border border-gray-300 rounded w-1/3 ">
      Partie corrections
      <ul v-if="solutions.length >0" class="divide-y divide-gray-100">
        <li v-for="solution in solutions" :key="solution.id" class="flex justify-between gap-x-6 py-5">
          <div class="flex min-w-0 gap-x-4">
            <div class="min-w-0 flex-auto">
              <p class="text-sm/6 font-semibold text-gray-900">
                {{ solution.exercice?.titre || 'Exercice sans titre'}}
              </p>
              <p class="mt-1 truncate text-xs/5 text-gray-500">
                Soumis le {{ formatDate(solution.date_a_soumettre) }}
              </p>
              <p v-if="solution.note" class="text-xs font-bold mt-1">
                Note : {{ solution.note }}/20
              </p>
            </div>
          </div>

          <div>
            <a v-if="solution.fichier && solution.fichier.url" :href="solution.fichier.url" target="_blank">
              Voir
            </a>
            <span v-else class="text-gray-500 text-xs">
              Fichier non disponible
            </span>
          </div>

        </li>
      </ul>
      <p v-else class="text-sm text-gray-500">
        Aucune soumission récente
      </p>
    
    </div>
  </div>


  <!-- Bloc de pagination -->
   <div v-if="pagination.total_pages " class="flex justify-center mt-8 mb-12">
    <nav class="flex items-center gap-x-1">
      <button @click="fetchExercices(pagination.current_page - 1)" :disabled="pagination.current_page === 1" class="min-h-[38px] min-w-[38px] py-2 px-2.5 inline-flex justify-center items-center gap-x-2 text-sm rounded-lg border border-gray-300 text-gray-800 hover:bg-gray-100 disabled:opacity-50">
        Précédent
      </button>
      <button v-for="page in pagination.total_pages" :key="page" @click="fetchExercices(page)"  :class="{' text-black': pagination.current_page === page, 'border-gray-300 text-gray-800 hover:bg-gray-100': pagination.current_page !== page}" class="min-h-[38px] min-w-[38px] flex justify-center items-center py-2 px-3 text-sm rounded-lg">
        {{ page }}
      </button>
      <button @click="fetchExercices(pagination.current_page + 1)" :disabled="pagination.current_page === pagination.total_pages" class="min-h-[38px] min-w-[38px] py-2 px-2.5 inline-flex justify-center items-center gap-x-2 text-sm rounded-lg border border-gray-300 text-gray-800 hover:bg-gray-100 disabled:opacity-50">
        Suivant
      </button>
    </nav>
   </div>

</template>
  
<script>

import axios from 'axios';
import {format, parseISO} from 'date-fns';
import {fr} from 'date-fns/locale';


export default {
  data() {
    return {
      exercices: [],
      solutions: [],
      loading : false,
      error:null,
      userClasse:null,
      pagination: {
        current_page: 1,
        total_pages:1,
      },
    };
  },

  async created() {
    await this.fetchExercices();
    await this.fetchSolutions();
    await this.fetchUserData();
  },

  methods: {

    async fetchUserData() {

      try{
        const token = localStorage.getItem("token");
        const response = await axios.get("/api/user/",
          {
            headers:{
              "Authorization":`Token ${token}`,
              "Content-Type":"application/json"
            }
          }
        );
        this.user = response.data.user;
         
      } catch(err){
        this.error="Erreur de chargement de l'utilisateur";
      }
    },

    async fetchExercices(){

      this.loading = true;
      this.error =null;
      try{
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/exercices/liste/',{
          headers:{
            "Authorization": `Token ${token}`,
          },
        });
        this.exercices = response.data;

      } catch(err){
          console.error('Erreur de chargement des exercices', err);
          this.error = err.response?.data?.error || 'Erreur de chargement des exercices';
      }finally{this.loading=false;}
    },

    async fetchSolutions(){
      try{
        const response = await axios.get('/');
        this.solutions = response.data;
      } catch (err){
        console.error('Erreur de chargement des solutions', err);
      }
    }, 

    formatDate(dateString){
      if (!dateString) return 'Date non disponible'
      try{
        return format(parseISO(dateString), 'PPpp', {locale:fr});
      } catch(error){
        console.error('Erreur de formatage des dates', error);
        return 'Format de date invalide';
      } 
    },

    telechargerFichier(url){
      const link = document.createElement('a');
      link.href=url;
      const filename = url.split('/').pop() || 'exercice';
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
   },

  },
};
</script>
  
<style scoped>
/* Styles spécifiques au dashboard */
</style>