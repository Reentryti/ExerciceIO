<template>
    <div class="container mx-auto p-4">
      <!-- Navigation breadcrumb -->
      <nav class="flex mb-4" aria-label="Breadcrumb">
        <ol class="inline-flex items-center space-x-1 md:space-x-2">
          <li v-if="currentView !== 'classes'" class="inline-flex items-center cursor-pointer hover:text-blue-600" @click="backToClasses">
            <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
            </svg>
            Classes
          </li>
          <li v-if="currentView === 'solutions'" class="inline-flex items-center cursor-pointer hover:text-blue-600" @click="backToExercices">
            <svg class="w-4 h-4 mx-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
            {{ selectedClasse.nom }}
          </li>
          <li v-if="currentView === 'solutions'" class="inline-flex items-center">
            <svg class="w-4 h-4 mx-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
            {{ selectedExercice.titre }}
          </li>
        </ol>
      </nav>
  
      <!-- Vue des classes -->
      <div v-if="currentView === 'classes'">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">Liste des classes</h2>
        <div v-if="loading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
        </div>
        <div v-else>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="classe in classes" :key="classe.id" @click="selectClasse(classe)" class="p-4 border rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer bg-white">
              <h3 class="font-semibold text-lg">{{ classe.nom }}</h3>
              <p class="text-gray-500 text-sm mt-1">{{ classe.etudiants_count }} étudiants</p>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Vue des exercices -->
      <div v-if="currentView === 'exercices'">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">Exercices pour {{ selectedClasse.nom }}</h2>
        <div v-if="loading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
        </div>
        <div v-else>
          <div v-if="exercices.length === 0" class="text-center py-8 text-gray-500">
            Aucun exercice pour cette classe
          </div>
          <div class="space-y-4">
            <div v-for="exercice in exercices" :key="exercice.id" @click="selectExercice(exercice)" class="p-4 border rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer bg-white">
              <div class="flex justify-between items-start">
                <h3 class="font-semibold text-lg">{{ exercice.titre }}</h3>
                <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                  {{ exercice.solutions_count }} solutions
                </span>
              </div>
              <p class="text-gray-600 mt-2">{{ exercice.description }}</p>
              <div class="flex justify-between text-sm text-gray-500 mt-3">
                <span>Créé le {{ formatDate(exercice.date_creation) }}</span>
                <span>Date limite: {{ formatDate(exercice.date_limite) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Vue des solutions -->
      <div v-if="currentView === 'solutions'">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold text-gray-800">
            Solutions pour "{{ selectedExercice.titre }}"
          </h2>
          <button @click="correctWithDeepSeek" class="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors":disabled="loading">
            <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span v-else class="flex items-center">
              <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
              Corriger toutes avec DeepSeek
            </span>
          </button>
        </div>
  
        <div v-if="loading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
        </div>
        <div v-else>
          <div v-if="solutions.length === 0" class="text-center py-8 text-gray-500">
            Aucune solution pour cet exercice
          </div>
          <div class="bg-white shadow rounded-lg overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Étudiant</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date soumission</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Note</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="solution in solutions" :key="solution.id">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center">
                        <span class="text-gray-600">{{ solution.etudiant_nom.charAt(0) }}</span>
                      </div>
                      <div class="ml-4">
                        <div class="text-sm font-medium text-gray-900">{{ solution.etudiant_nom }}</div>
                        <div class="text-sm text-gray-500">{{ solution.etudiant_email }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatDate(solution.date_soumission) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <input v-model="solution.note" type="number" min="0" max="20" step="0.5" @change="updateNote(solution)" class="w-20 p-1 border rounded focus:ring-blue-500 focus:border-blue-500" :class="{'bg-yellow-50': solution.note_updated}">
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div class="flex space-x-2">
                      <a :href="solution.fichier" target="_blank" class="text-blue-600 hover:text-blue-900 flex items-center">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                        </svg>
                        Voir
                      </a>
                      <button @click="correctSolutionWithDeepSeek(solution.id)" class="text-blue-600 hover:text-blue-900 flex items-center" :disabled="loading">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                        </svg>
                        Corriger
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
  
      <!-- Notification d'erreur -->
      <div v-if="error" class="fixed bottom-4 right-4">
        <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 shadow-lg rounded">
          <div class="flex justify-between items-start">
            <div class="flex items-center">
              <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span class="font-semibold">Erreur</span>
            </div>
            <button @click="error = null" class="ml-4 text-red-700 hover:text-red-900">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
          <p class="mt-2">{{ error }}</p>
        </div>
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
      async fetchClasses() {
        this.loading = true;
        this.error = null;
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
          console.error('Erreur fetchClasses:', error);
          this.error = error.response?.data?.message || "Erreur lors du chargement des classes";
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
          console.error('Erreur selectClasse:', error);
          this.error = error.response?.data?.message || "Erreur lors du chargement des exercices";
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
          console.error('Erreur fetchExercices:', error);
          throw error;
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
          //Flag pour les notes mises à jour
          this.solutions = response.data.map(sol => ({
            ...sol,
            note_updated: false
          }));
          this.currentView = 'solutions';
        } catch (error) {
          console.error("Erreur selectExercice:", error);
          this.error = error.response?.data?.message || "Erreur lors du chargement des solutions";
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
        if (!dateString) return 'Non spécifié';
        try {
          return format(new Date(dateString), 'dd/MM/yyyy HH:mm', { locale: fr });
        } catch(error) {
          console.error('Erreur formatDate:', dateString);
          return 'Date invalide';
        }
      },
          
      async updateNote(solution) {
        try {
          const token = localStorage.getItem('token');
          await axios.post(`http://localhost:8000/exercices/solutions/${solution.id}/attribuer-note/`, {
            valeur: solution.note
          }, {
            headers: {
              "Authorization": `Token ${token}`,
              "Content-Type": "application/json"
            }
          });
          // Marquer comme mise à jour
          solution.note_updated = true;
          setTimeout(() => {
            solution.note_updated = false;
          }, 2000);
        } catch (error) {
          console.error("Erreur updateNote:", error);
          this.error = error.response?.data?.message || "Erreur lors de la mise à jour de la note";
        }
      },
  
      async correctSolutionWithDeepSeek(solutionId) {
        try {
          this.loading = true;
          const token = localStorage.getItem('token');
  
          const response = await axios.post(
            `http://localhost:8000/corrections/solutions/${solutionId}/corriger/`,
            {},
            {
              headers: {
                "Authorization": `Token ${token}`,
                "Content-Type": "application/json"
              }
            }
          );
  
          const solutionIndex = this.solutions.findIndex(s => s.id === solutionId);
          if (solutionIndex !== -1) {
            this.solutions[solutionIndex].note = response.data.note;
            this.solutions[solutionIndex].note_updated = true;
            setTimeout(() => {
              this.solutions[solutionIndex].note_updated = false;
            }, 2000);
          }
        } catch (error) {
          console.error("Erreur correctSolutionWithDeepSeek:", error);
          this.error = error.response?.data?.message || "Erreur lors de la correction";
        } finally {
          this.loading = false;
        }
      },
  
      async correctWithDeepSeek() {
        try {
          this.loading = true;
          const token = localStorage.getItem('token');
          
          await axios.post(
            `http://localhost:8000/corrections/exercices/${this.selectedExercice.id}/corriger-toutes/`,
            {},
            {
              headers: {
                "Authorization": `Token ${token}`,
                "Content-Type": "application/json"
              }
            }
          );
          
          //Recharge les solutions après correction
          await this.selectExercice(this.selectedExercice);
        } catch (error) {
          console.error("Erreur correctWithDeepSeek:", error);
          this.error = error.response?.data?.message || "Erreur lors de la correction globale";
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