<template>
  <div class="container mx-auto p-4">
      
    <!-- Liste des classes -->
    <div v-if="currentView === 'classes'">
      <h2 class="text-2xl font-bold mb-4">
        Liste des classes
      </h2>
      <ul class="space-y-2">
        <li v-for="classe in classes" :key="classe.id" @click="selectClasse(classe)" class="p-3 border rounded hover:bg-gray-100 cursor-pointer">
          {{ classe.nom }}
        </li>
      </ul>
    </div>
  
    <!-- Liste des exercices -->
    <div v-if="currentView === 'exercices'">
      <button @click="backToClasses" class="mb-4 flex items-center text-blue-600">
        <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
        </svg>
          Retour aux classes
      </button>
      
      <h2 class="text-2xl font-bold mb-4">
        Exercices pour {{ selectedClasse.nom }}
      </h2>
      <ul class="space-y-2">
        <li v-for="exercice in exercices" :key="exercice.id" @click="selectExercice(exercice)" class="p-3 border rounded hover:bg-gray-100 cursor-pointer">
          {{ exercice.titre }}
        </li>
      </ul>
    </div>
  
    <!-- Liste des solutions -->
    <div v-if="currentView === 'solutions'">
      <button @click="backToExercices" class="mb-4 flex items-center text-blue-600">
        <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
        </svg>
        Retour aux exercices
      </button>
      
      <h2 class="text-2xl font-bold mb-4">
          Solutions de {{ selectedExercice.titre }}
      </h2>
      
      <div class="mb-4">
        <button @click="correctWithDeepSeek" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          Corriger avec DeepSeek
        </button>
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full bg-white">
          <thead>
            <tr>
              <th class="py-2 px-4 border-b">Étudiant</th>
              <th class="py-2 px-4 border-b">Date soumission</th>
              <th class="py-2 px-4 border-b">Note</th>
              <th class="py-2 px-4 border-b">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="solution in solutions" :key="solution.id">
              <td class="py-2 px-4 border-b">{{ solution.etudiant_nom }}</td>
              <td class="py-2 px-4 border-b">{{ formatDate(solution.date_soumission) }}</td>
              <td class="py-2 px-4 border-b">
                <input v-model="solution.note" type="number" min="0" max="20" step="0.5" @change="updateNote(solution)" class="w-20 p-1 border rounded">
              </td>
              <td class="py-2 px-4 border-b">
                <a :href="solution.fichier" target="_blank" class="text-blue-600 hover:underline mr-2">
                  Voir fichier
                </a>
                <button @click="correctSolutionWithDeepSeek(solution.id)" class="text-blue-600 hover:underline">
                  Corriger
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  
    <!-- Chargement -->
    <div v-if="loading" class="text-center py-8">
      <p>Chargement en cours...</p>
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';
  
export default {
  data() {
    return {
      currentView: 'classes',
      classes: [],
      exercices: [],
      solutions: [],
      selectedClasse: null,
      selectedExercice: null,
      loading: false,
      error: null
    }
  },
  methods: {
    //Récupération des classes
    async fetchClasses() {
      this.loading = true;
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/api/professeur/classes/', {
          headers: {
            "Authorization": `Token ${token}`,
            "Content-Type": "application/json"
          },
        });
        this.classes = response.data;
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    
    async selectClasse(classe) {
      this.selectedClasse = classe;
      this.loading = true;
      this.error = null;
      try {
        await this.fetchExercices(classe.id);
        this.currentView = 'exercices';
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    
    async fetchExercices(classeId) {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`http://localhost:8000/exercices/professeur/classes/${classeId}/exercices/`, {
          headers: { 
            "Authorization": `Token ${token}`, 
            "Content-Type": "application/json"
          }
        });
        this.exercices = response.data;
      } catch (error) {
        console.error('Erreur:', error);
      }
    },

    async selectExercice(exercice) {
      this.selectedExercice = exercice;
      this.loading = true;
      this.error = null;
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`http://localhost:8000/exercices/${exercice.id}/solutions/`, {
          headers: {
            "Authorization": `Token ${token}`,
            "Content-Type": "application/json"
          }
        });
        console.log('Solutions from API', response.data);
        this.solutions = response.data;
        this.currentView = 'solutions';
      } catch (error) {
        this.error = "Erreur du chargement des solutions";
        console.error("Erreur de selection des solutions", error.response?.data || error.message);
      } finally {
        this.loading = false;
      }
    },

    backToClasses() {
      this.currentView = 'classes';
      this.selectedClasse = null;
      this.exercices = [];
    },
    
    backToExercices() {
      this.currentView = 'exercices';
      this.selectedExercice = null;
      this.solutions = [];
    },
    
    formatDate(dateString) {
      if (!dateString) return 'No date';
      try {
        return format(new Date(dateString), 'dd/MM/yyyy HH:mm', { locale: fr });
      } catch(error) {
        console.error('format date invalide:', dateString);
        return 'Date invalide';
      }
    },
        
    async updateNote(solution) {
      try {
        const token = localStorage.getItem('token');
        await axios.post(`http://localhost:8000/api/solutions/${solution.id}/attribuer-note/`, {
          valeur: solution.note
        }, {
          headers: {
            "Authorization": `Token ${token}`,
            "Content-Type": "application/json"
          }
        });
      } catch (error) {
        console.error("Erreur mise à jour note:", error);
      }
    },

    async correctSolutionWithDeepSeek(solutionId) {
      try {
        this.loading = true;
        const token = localStorage.getItem('token');

        const response = await axios.post(`http://localhost:8000/corrections/solutions/${solutionId}/corriger/`,
          {}, {
            headers: {
              "Authorization": `Token ${token}`,
              "Content-Type": "application/json"
            }
          });

        const solutionIndex = this.solutions.findIndex(s => s.id === solutionId);
        if (solutionIndex !== -1) {
          this.solutions[solutionIndex].note = response.data.note;
        }
        alert('Correction effectuée avec succès');

      } catch (error) {
        console.error("Erreur lors de la correction", error);
        alert('Erreur lors de la correction: ' + (error.response?.data?.message || error.message));
      } finally {
        this.loading = false;
      }
    },

    async correctWithDeepSeek() {
      try {
        this.loading = true;
        const token = localStorage.getItem('token');
        
        // Updated URL path to match Django URL structure
        const response = await axios.post(`http://localhost:8000/corrections/exercices/${this.selectedExercice.id}/corriger-toutes/`,
          {}, {
            headers: {
              "Authorization": `Token ${token}`,
              "Content-Type": "application/json"
            }
          }
        );
        
        await this.selectExercice(this.selectedExercice);
        alert('Toutes les solutions sont corrigées');
      } catch (error) {
        console.error("Erreur de la correction globale", error);
        alert('Erreur lors de la correction: ' + (error.response?.data?.message || error.message));
      } finally {
        this.loading = false;
      }
    }
  
  },
  created() {
    this.fetchClasses();
  }
};
</script>
  
<style scoped>
/* Styles personnalisés */
</style>