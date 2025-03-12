<template>
    <div class="w-full md:w-2/3 bg-blue-100 rounded-lg">
      <!-- Formulaire pour déposer un exercice (visible uniquement par les professeurs) -->
      <div v-if="user.role === 'professeur'" class="p-12 ">
        <h2 class="text-lg font-light">Déposer un nouvel exercice</h2>
        <form @submit.prevent="deposerExercice">
          <div class=" mt-8">
            <label for="titre" class="block font-light mb-3">Titre exercice</label>
            <input v-model="nouvelExercice.titre" placeholder="Nom de l'exercice" class="p-2 rounded bg-gray-100 outline-black outline-1 focus:outline-2 focus:outline-blue-500 " type="text" id="titre" required />
          </div>
          <div class="mt-5">
            <label for="description" class="block mb-3">Instructions</label>
            <textarea v-model="nouvelExercice.description" placeholder="Consignes supplémentaires" class="block w-full rounded-md bg-gray-100 px-5 py-5 text-gray-900 outline-1 -outline-offset-1 outline-black placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 " id="description" required></textarea>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 mt-6">
            <div class="p-4">
              <label for="date" class="block text-sm font-medium text-gray-700">Sélectionner une date :</label>
              <input type="date" id="date" v-model="selectedDate"  class="mt-1 p-2 border rounded w-full"/>
            </div>
            <div class="w-full p-4">
              <label for="classes" class="block">Classes </label>
              <select v-model="nouvelExercice.classes" id="classes" required class="block appearance-none w-full bg-gray-100 text-black py-3 px-4 pr-8 rounded">
                <option value="">---Veuillez choisir une classe-----</option>
                <option v-for="classe in classes" :key="classe.id" :value="classe.id">
                  {{ classe.nom }}
                </option>
              </select>
            </div>
          </div>
          <div class="border mt-8">
            <input type="file" id="fichier" @change="onFileChange" class="text-white"/>
          </div>
          <button type="submit" class="mt-4 border bg-blue-500 py-2 px-4 rounded-xl" :disabled="isLoading">
            <span v-if="isLoading">Chargement...</span>
            <span v-else>Déposer</span>
          </button>
        </form>
      </div>
  
      <!-- Liste des exercices -->
      <div class="liste-exercices">
        <h2>Exercices</h2>
        <ul>
          <li v-for="exercice in exercices" :key="exercice.id" class="exercice-item">
            <h3>{{ exercice.titre }}</h3>
            <p>{{ exercice.description }}</p>
            <p>Classes : {{ exercice.classes.join(', ') }}</p>
            <a v-if="exercice.fichier" :href="exercice.fichier" target="_blank">Télécharger le fichier</a>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'Exercices',
    data() {
      return {
        user: {
          id: 1,  // Remplacez par l'ID de l'utilisateur connecté
          role: 'professeur',  // Remplacez par le rôle de l'utilisateur connecté
        },
        classes: [],  // Liste des classes récupérées depuis l'API
        exercices: [],  // Liste des exercices récupérés depuis l'API
        nouvelExercice: {
          titre: '',
          description: '',
          classes: [],
          fichier: null,
          dateLimite:'',
        },
        selectedDate:'',
      };
    },
    created() {
      this.chargerClasses();
      this.chargerExercices();
    },
    methods: {
      async chargerClasses() {
        try {
          const response = await axios.get('http://127.0.0.1:8000/api/classes/');
          this.classes = response.data;
        } catch (error) {
          console.error('Erreur lors du chargement des classes:', error);
        }
      },
      async chargerExercices() {
        try {
          const url = this.user.role === 'professeur'
            ? 'http://127.0.0.1:8000/exercices/'
            : 'http://127.0.0.1:8000/exercices/liste/';
          const response = await axios.get(url);
          this.exercices = response.data;
        } catch (error) {
          console.error('Erreur lors du chargement des exercices:', error);
        }
      },
      onFileChange(event) {
        this.nouvelExercice.fichier = event.target.files[0];
      },

      async deposerExercice() {
        const formData = new FormData();
        formData.append('titre', this.nouvelExercice.titre);
        formData.append('description', this.nouvelExercice.description);
        formData.append('classes', JSON.stringify(this.nouvelExercice.classes));
        formData.append('dateLimite', this.selectedDate);
        if (this.nouvelExercice.fichier) {
          formData.append('fichier', this.nouvelExercice.fichier);
        }
  
        try {
          const response = await axios.post('http://127.0.0.1:8000/exercices/upload/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
          this.exercices.push(response.data);  // Ajouter le nouvel exercice à la liste
          this.nouvelExercice = { titre: '', description: '', classes: [], fichier: null };  // Réinitialiser le formulaire
          alert('Exercice déposé avec succès !');
        } catch (error) {
          console.error('Erreur lors du dépôt de l\'exercice:', error.response?.data || error.message);
          alert('Erreur lors du dépôt de l\'exercice.');
        }
      },
    },
  };
  </script>
  
  <style scoped>
  </style>