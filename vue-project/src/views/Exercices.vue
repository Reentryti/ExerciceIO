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
  <div class="flex flex-col gap-10 md:flex-row-reverse mx-5 md:mx-20">
    
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
    <div class="hidden md:inline border border-gray-300 rounded w-1/3 p-4">
      <h3 class="font-semibold text-lg mb-3">Corrections récentes</h3>
      <ul v-if="corrections.length > 0" class="divide-y divide-gray-100">
        <li v-for="correction in limitedCorrections" :key="correction.id" class="flex justify-between gap-x-6 py-5">
          <div class="flex min-w-0 gap-x-4">
            <div class="min-w-0 flex-auto">
              <p class="text-sm/6 font-semibold text-gray-900">
                {{ correction.solution?.exercice?.titre || 'Exercice sans titre'}}
              </p>
              <p class="mt-1 truncate text-xs/5 text-gray-500">
                Corrigé le {{ formatDate(correction.date_correction) }}
              </p>
              <p v-if="correction.note" class="text-xs font-bold mt-1">
                Note : {{ correction.note }}/20
              </p>
              <p class="text-xs text-gray-500 mt-1">
                <span v-if="correction.provider === 'DEEPSEEK'" class="rounded-full bg-blue-100 px-2 py-1">IA</span>
                <span v-else class="rounded-full bg-green-100 px-2 py-1">Manuel</span>
              </p>
            </div>
          </div>

          <div>
            <router-link :to="`/correction/${correction.id}/`" class="text-red-400 hover:text-red-600 text-sm">
              Voir le détail
            </router-link>
          </div>

        </li>
      </ul>
      <p v-else class="text-sm text-gray-500">
        Aucune correction récente
      </p>
      
      <div v-if="corrections.length > correctionsLimit" class="mt-4 text-center">
        <button @click="showMoreCorrections" class="text-sm text-red-400 hover:text-red-600">
          Voir plus
        </button>
      </div>
    </div>
  </div>


  <!-- Bloc de pagination -->
   <div v-if="pagination.total_pages > 1" class="flex justify-center mt-8 mb-12">
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
      corrections: [],
      correctionsLimit: 5,
      loading : false,
      error: null,
      userClasse: null,
      pagination: {
        current_page: 1,
        total_pages: 1,
      },
    };
  },

  computed: {
    limitedCorrections() {
      return this.corrections.slice(0, this.correctionsLimit);
    }
  },

  async created() {
    await this.fetchExercices();
    await this.fetchCorrections();
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

    async fetchExercices(page = 1){
      this.loading = true;
      this.error = null;
      try{
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/exercices/liste/', {
          headers: {
            "Authorization": `Token ${token}`,
          },
          params: {
            page: page
          }
        });
        this.exercices = response.data.results || response.data;
        
        // Mise à jour de la pagination si disponible
        if (response.data.pagination) {
          this.pagination = response.data.pagination;
        } else {
          this.pagination.current_page = 1;
          this.pagination.total_pages = 1;
        }

      } catch(err){
        console.error('Erreur de chargement des exercices', err);
        this.error = err.response?.data?.error || 'Erreur de chargement des exercices';
      } finally {
        this.loading = false;
      }
    },

    async fetchCorrections(){
      try{
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/corrections/', {
          headers: {
            "Authorization": `Token ${token}`,
          }
        });
        this.corrections = response.data;
        console.log('Corrections chargées:', this.corrections);
      } catch (err){
        console.error('Erreur de chargement des corrections', err);
        // Solution de secours : données de démonstration
        this.corrections = [
          {
            id: 1,
            note: 15,
            commentaires: "Bon travail, quelques erreurs mineures",
            date_correction: "2025-04-28T14:30:00Z",
            provider: "DEEPSEEK",
            solution: {
              id: 101,
              exercice: {
                id: 201,
                titre: "Exercice de mathématiques"
              }
            }
          },
          {
            id: 2,
            note: 18,
            commentaires: "Excellent travail",
            date_correction: "2025-04-25T10:15:00Z",
            provider: "MANUAL",
            solution: {
              id: 102,
              exercice: {
                id: 202,
                titre: "Exercice de français"
              }
            }
          },
          {
            id: 3,
            note: 12,
            commentaires: "Des concepts importants manquent",
            date_correction: "2025-04-22T16:45:00Z",
            provider: "DEEPSEEK",
            solution: {
              id: 103,
              exercice: {
                id: 203,
                titre: "Exercice de physique"
              }
            }
          }
        ];
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
      link.href = url;
      const filename = url.split('/').pop() || 'exercice';
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },

    showMoreCorrections() {
      this.correctionsLimit += 5;
    }
  },
};
</script>
  
<style scoped>
/* Styles spécifiques au dashboard */
</style>