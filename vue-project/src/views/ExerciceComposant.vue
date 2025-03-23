<template>
    <div class="min-h-screen bg-gray-100 p-6">
      <!-- Affichage des détails de l'exercice -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h1 class="text-2xl font-bold mb-4">{{ exercice.titre }}</h1>
        <p class="text-gray-700 mb-4">{{ exercice.description }}</p>
        <p class="text-sm text-gray-500">
          Date limite : {{ formatDate(exercice.date_a_soumettre) }}
        </p>
        <div v-if="exercice.fichier" class="mt-4">
          <a :href="exercice.fichier" target="_blank" class="text-blue-500 hover:underline">
            Télécharger le fichier de l'exercice
          </a>
        </div>
      </div>
  
      <!-- Formulaire de dépôt de solution -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-bold mb-4">Déposer votre solution</h2>
        <form @submit.prevent="deposerSolution">
          <!-- Fichier de la solution -->
          <div class="mb-4">
            <label for="fichier" class="block text-sm font-medium text-gray-700">Fichier de la solution</label>
            <input type="file" id="fichier" @change="onFileChange" class="mt-1 block w-full p-2 border border-gray-300 rounded-md" required />
          </div>
  
          <!-- Commentaire (optionnel) -->
          <div class="mb-4">
            <label for="commentaire" class="block text-sm font-medium text-gray-700">Commentaire (optionnel)</label>
            <textarea id="commentaire" v-model="solution.commentaire" class="mt-1 block w-full p-2 border border-gray-300 rounded-md" rows="3"></textarea>
          </div>
  
          <!-- Bouton de soumission -->
          <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">
            Déposer la solution
          </button>
        </form>
      </div>
    </div>
  </template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      exercice: {},  // Détails de l'exercice sélectionné
      solution: {
        fichier: null,  // Fichier de la solution
        commentaire: '',  // Commentaire optionnel
      },
      error: null,  // Message d'erreur
    };
  },
  created() {
    this.chargerExercice();  // Charger les détails de l'exercice au montage du composant
  },
  methods: {
    // Charger les détails de l'exercice
    async chargerExercice() {
      const exerciceId = this.$route.params.id;  // Récupérer l'ID de l'exercice depuis l'URL
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`http://localhost:8000/exercices/${exerciceId}/`, {
          headers: {
            'Authorization': `Token ${token}`,
          },
        });
        this.exercice = response.data;
      } catch (error) {
        console.error('Erreur lors du chargement de l\'exercice:', error);
        this.error = 'Impossible de charger l\'exercice. Veuillez réessayer.';
      }
    },

    // Gérer le changement de fichier
    onFileChange(event) {
      this.solution.fichier = event.target.files[0];
    },

    // Déposer la solution
    async deposerSolution() {
      if (!this.solution.fichier) {
        this.error = 'Veuillez sélectionner un fichier.';
        return;
      }

      const formData = new FormData();
      formData.append('fichier', this.solution.fichier);
      formData.append('commentaire', this.solution.commentaire);
      formData.append('exercice', this.exercice.id);

      try {
        const token = localStorage.getItem('token');
        const response = await axios.post('http://localhost:8000/solutions/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Token ${token}`,
          },
        });
        alert('Solution déposée avec succès !');
        this.solution = { fichier: null, commentaire: '' };  // Réinitialiser le formulaire
      } catch (error) {
        console.error('Erreur lors du dépôt de la solution:', error);
        this.error = 'Erreur lors du dépôt de la solution. Veuillez réessayer.';
      }
    },

    // Formater la date
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
      });
    },
  },
};
</script>
