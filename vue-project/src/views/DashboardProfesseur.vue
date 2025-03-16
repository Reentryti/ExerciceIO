<template>
  <div class="min-h-full">
    <header class="bg-white shadow-sm">
      <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold tracking-tight text-gray-900">Tableau de bord</h1>
      </div>
    </header>
    <main>
      <div class="mx-auto max-w-7xl">
        <!-- Bloc principal -->
        <div class=" grid md:grid-cols-3 grid-cols-1 gap-8 p-4">
          <!-- Sous-bloc : Mes Exercices -->
          <div class="col-span-1 row-span-2 ring rounded-lg py-8 px-6">
            <h2 class="text-xl font-semibold mb-4">Mes Exercices</h2>
            <div v-if="exercices.length > 0">
              <ul class="space-y-2">
                <li v-for="exercice in exercices" :key="exercice.id" class="p-2 bg-gray-100 rounded-lg">
                  {{ exercice.titre }}
                </li>
              </ul>
            </div>
            <p v-else class="p-2 bg-gray-100 rounded-lg">Aucun exercice créé.</p>
            <div>
              <button @click="popupExercice">
                Déposer un exercice
              </button>
              <!-- Popup Exercice -->
              <div v-if="popupOpen" class="">
                <div class="">
                  <button class="" @click="popupClose">×</button>
                  <Exercice @exercise-added="handleExerciseAdded" />
                </div>
              </div>
            </div>
          </div>

          <!-- Sous-bloc : Corrections -->
          <div class="col-span-2 row-span-1 shadow-md rounded-lg py-8 px-6">
            <h2 class="text-xl font-semibold mb-4">Corrections</h2>
            <div v-if="corrections.length > 0">
              <ul class="space-y-2">
                <li v-for="correction in corrections" :key="correction.id" class="p-2 bg-gray-100 rounded-lg">
                  <p>{{ correction.exercice.titre }} - {{ correction.etudiant.username }}</p>
                  <p>Statut : {{ correction.statut }}</p>
                </li>
              </ul>
            </div>
            <p v-else class="p-2 bg-gray-100 rounded-lg">Aucune correction en attente.</p>
          </div>

          <!-- Sous-bloc : Mes classes -->
          <div class="col-span-1 row-span-1 shadow-md rounded-lg py-8 px-6">
            <h2 class="text-xl font-semibold mb-4">Mes classes</h2>
            <div v-if="loading" class="text-center">
              <p>Chargement...</p>
            </div>
            <ul v-else-if="classes.length > 0" class="space-y-2">
              <li v-for="classe in classes" :key="classe.id" class="p-2 bg-red-200 rounded-lg">
                {{ classe.nom }}
              </li>
            </ul>
            <p v-else class="p-2 bg-gray-100 rounded-lg">Aucune classe affectée.</p>
          </div>

          <!-- Sous-bloc : Moyenne des classes -->
          <div class="col-span-1 row-span-1 shadow-md rounded-lg py-8 px-6">
            <h2 class="text-xl font-semibold mb-4">Moyenne des classes</h2>
            <div v-if="moyennes.length > 0">
              <ul class="space-y-2">
                <li v-for="moyenne in moyennes" :key="moyenne.classe.id" class="p-2 bg-gray-100 rounded-lg">
                  <p>{{ moyenne.classe.nom }} : {{ moyenne.moyenne }}/20</p>
                </li>
              </ul>
            </div>
            <p v-else class="p-2 bg-gray-100 rounded-lg">Aucune moyenne disponible.</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>


<script>
import axios from 'axios';
import Exercice from './Exercice.vue';

export default {
  components:{
    Exercice,
  },
  data() {
    return {
      popupOpen:false,
      classes: [],
      exercices: [],
      corrections: [],
      moyennes: [],
      loading: true,
      error: null
    };
  },
  mounted() {
    this.fetchClasses();
    
  },
  methods: {
    async fetchClasses() {
      this.loading = true;
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/api/professeur/classes', {
          headers: {
            "Authorization": `Token ${token}`,
            "Content-Type": "application/json"
          },
        });
        this.classes = response.data;
      } catch (error) {
        console.error('Erreur lors de la récupération des classes:', error);
        this.error = 'Impossible de charger les classes. Veuillez réessayer plus tard.';
      } finally {
        this.loading = false;
      }
    },
    popupExercice(){
      this.popupOpen = true;
    },
    popupClose(){
      this.popupOpen = false;
    },
    handleExerciseAdded(){
      this.popupClose();
    },
  }
};
</script>