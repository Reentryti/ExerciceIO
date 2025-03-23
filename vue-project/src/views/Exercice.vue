<template>
    <div class="w-full bg-white rounded-lg shadow-lg">
      <!-- Formulaire pour dépot d'exercice  -->
      <div v-if="user.role === 'professeur'" class="p-10">
        <h2 class=" bg-gradient-to-r from-red-500 to-violet-500 bg-clip-text text-3xl font-extrabold text-transparent">Dépôt Exercice</h2>
        <!-- Formulaire -->
        <form @submit.prevent="deposerExercice">
          <!-- Titre de l'exercice -->
          <div class=" mt-8">
            <label for="titre" class="block font-light mb-3">Titre exercice</label>
            <input v-model="nouvelExercice.titre" placeholder="Nom de l'exercice" class="p-2 rounded bg-gray-100 outline-black outline-1 focus:outline-2  " type="text" id="titre" required />
          </div>
          <!-- Instructions de l'exercice -->
          <div class="mt-5">
            <label for="description" class="block mb-3">Instructions</label>
            <textarea v-model="nouvelExercice.description" placeholder="Voici ce qu'il y a à faire" class="block w-full rounded-md bg-gray-100 p-2  outline-1 -outline-offset-1 outline-black placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 " id="description" required></textarea>
          </div>
          <!-- Date et Classe  -->
          <div class="grid grid-cols-1 gap-4 md:grid-cols-2 mt-6">
            <!-- Date de soumission -->
            <div class="">
              <label for="date" class="block mb-3">Date Limite</label>
              <input type="date" id="date" v-model="selectedDate" required class="p-3 border rounded w-full bg-gray-100"/>
            </div>
            <!-- Classe affectée -->
            <div class="w-full">
              <label for="classes_affected" class="block mb-3">Classes affectées</label>
              <select v-model="nouvelExercice.classes_affected" id="classes_affected" required class="border w-full bg-gray-100 text-black p-3 rounded" multiple>
                <option value="">---Veuillez choisir une classe-----</option>
                <option v-for="classe in classes" :key="classe.id" :value="Number(classe.id)">
                  {{ classe.nom }}
                </option>
              </select>
            </div>
          </div>
          <!-- Upload -->
          <div class="border mt-8">
            <input type="file" @change="onFileChange" class="hidden" ref="fileUpload" accept=".txt, .pdf"/>
            <button type="button" @click="openFile" class="bg-red-400 text-white rounded-lg px-4 py-2 transition duration-300">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
              </svg>
              <span>Choisir un fichier</span>
            </button>
            <p v-if="selectedFile" class="text-black">
              {{ selectedFile.name }}
            </p>
          </div>
          <!-- Bouton d'envoi -->
          <button type="submit" class="mt-4 border bg-gray-500 text-white py-2 px-4 rounded-xl hover:bg-red-400 hover:font-bold" :disabled="isLoading">
            
            <span >Déposer</span>
          </button>
        </form>
        <div v-if="error" class="text-red-500 mt-4">
          {{ error }}
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'Exercices',
    data() {
      return {
        isLoading: false,
        selectedFile: null,
        user: {
          id: 1,  // Remplacez par l'ID de l'utilisateur connecté
          role: 'professeur',  // Remplacez par le rôle de l'utilisateur connecté
        },
        classes: [],  // Liste des classes récupérées depuis l'API
        exercices: [],  // Liste des exercices récupérés depuis l'API
        nouvelExercice: {
          titre: '',
          description: '',
          classes_affected: [],
          fichier: null,
          dateLimite: '',
        },
        selectedDate: '',
        error: null,  // Ajout d'un message d'erreur
      };
    },

    created() {
      this.chargerClasses();
      //this.chargerExercices();
    },
    methods: {
      async chargerClasses() {

        try {
          const token = localStorage.getItem('token');
          const response = await axios.get('http://127.0.0.1:8000/api/professeur/classes',{

           headers:{
            'Authorization':`Token ${token}`
           }
          });
          this.classes = response.data;
        } catch (error) {
          console.error('Erreur lors du chargement des classes:', error);
        }
      },
      openFile(){
        this.$refs.fileUpload.click();
      },

      onFileChange(event) {
        const file = event.target.files[0];
        if(file){
          this.selectedFile = file;
          this.nouvelExercice.fichier = file;
        }
      },
      //Function 
      async deposerExercice() {
        this.isLoading = true;
        this.error = null;  // Réinitialiser l'erreur

        const formData = new FormData();
        formData.append('titre', this.nouvelExercice.titre);
        formData.append('description', this.nouvelExercice.description);
        // For multiple values, append each value separately
        this.nouvelExercice.classes_affected.forEach(classId => {
          formData.append('classes_affected', classId);
        }); // Correction du nom du champ
        formData.append('date_a_soumettre', this.selectedDate);
        if (this.nouvelExercice.fichier) {
          formData.append('fichier', this.nouvelExercice.fichier);
        }

        try {
          const token = localStorage.getItem('token');
          const response = await axios.post('http://127.0.0.1:8000/exercices/upload/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
              'Authorization': `Token ${token}`,
            },
            withCredentials: true,
          });
          this.exercices.push(response.data);  // Ajouter le nouvel exercice à la liste
          this.nouvelExercice = { titre: '', description: '', classes_affected: [], fichier: null };  // Réinitialiser le formulaire
          this.selectedFile = null;  // Réinitialiser le fichier sélectionné
          alert('Exercice déposé avec succès !');
          this.$emit('exercice-added', response.data);
        } catch (error) {
          console.error('Erreur lors du dépôt de l\'exercice:', error.response?.data || error.message);
          this.error = error.response?.data?.message || 'Erreur lors du dépôt de l\'exercice. Veuillez réessayer.';
        } finally {
          this.isLoading = false;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  </style>