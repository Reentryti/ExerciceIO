<template>
    <div class="min-h-screen bg-gray-100 p-6">
      <!-- Affichage des détails de l'exercice -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h1 class="text-2xl font-bold mb-4">{{ exercice.titre }}</h1>
        <p class="text-gray-700 mb-4">{{ exercice.description }}</p>
        <p class="text-sm text-gray-500">
          Date limite : {{ formatDate(exercice.date_a_soumettre) }}
        </p>


         <!-- Section du fichier de l'exercice avec prévisualisation -->
        <div v-if="exercice.fichier" class="mt-4">
          <div class="flex items-center space-x-4 mb-4">
            <!-- Telechargement de l'exercice -->
            <button @click="telechargerFichier(exercice.fichier)" class="flex items-center text-blue-500 hover:underline">
              <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
              </svg>
              Télécharger le fichier de l'exercice
            </button>
          </div>

          <!-- Prévisualisation du fichier -->
          <div class="border rounded-lg p-4 bg-gray-50">
            <h3 class="font-medium mb-2">Prévisualisation :</h3>
              
            <!-- Pour les PDF -->
            <div v-if="isPdfExercice" class="pdf-preview-container">        
              <embed :src="exercice.fichier + '#view=FitH'" type="application/pdf" class="w-full h-96 border"/>
              <p class="text-xs text-gray-500 mt-2">
                Si le PDF ne s'affiche pas
                <a :href="exercice.fichier" target="_blank">
                  Ouvrir dans un autre onglet
                </a>
              </p>
            </div>
 
            <!-- Pour les fichiers texte -->
            <div v-else-if="isTextExercice" class="bg-white p-4 rounded border">
              <pre class="whitespace-pre-wrap font-mono text-sm">{{ exerciceFileContent }}</pre>
            </div>
            
            <!-- Pour les autres types de fichiers -->
            <div v-else class="text-center py-8 text-gray-500">
              <svg class="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <p>Aucune prévisualisation disponible pour ce type de fichier</p>
            </div>
          </div>
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
      exerciceFileContent:'',
    };
  },
  computed:{
    isPdfExercice(){
      return this.exercice.fichier && this.exercice.fichier.toLowerCase().endsWith('.pdf');
    },
    isTextExercice(){
      return this.exercice.fichier && this.exercice.fichier.toLowerCase().endsWith('.txt');
    },
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
        
        if (this.isTextExercice){
          await this.loadTextFileContent(this.exercice.fichier);
        }

      } catch (error) {
        console.error('Erreur lors du chargement de l\'exercice:', error);
        this.error = 'Impossible de charger l\'exercice. Veuillez réessayer.';
      }
    },

    // Fonction de chargement fichier txt
    async loadTextFileContent(url){
      try{
        const response = await axios.get(url, { responseType:'text'});
        this.exerciceFileContent = response.data;
      
      }catch(error){
        console.error("Erreur lors du chargement du txt", error);
        this.exerciceFileContent = "Impossible de charger le fichier";
      }
    },

    //Fonction de telechargement des exercices
   telechargerFichier(url){
      const link = document.createElement('a');
      link.href=url;
      const filename = url.split('/').pop() || 'exercice';
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
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
