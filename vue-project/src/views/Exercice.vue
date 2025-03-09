<template>
    <div class="exercices-container">
      <!-- Formulaire pour déposer un exercice (visible uniquement par les professeurs) -->
      <div v-if="user.role === 'professeur'" class="form-container">
        <h2>Déposer un nouvel exercice</h2>
        <form @submit.prevent="deposerExercice">
          <div class="form-group">
            <label for="titre">Titre :</label>
            <input v-model="nouvelExercice.titre" type="text" id="titre" required />
          </div>
          <div class="form-group">
            <label for="description">Description :</label>
            <textarea v-model="nouvelExercice.description" id="description" required></textarea>
          </div>
          <div class="form-group">
            <label for="classes">Classes :</label>
            <select v-model="nouvelExercice.classes" id="classes" multiple>
              <option v-for="classe in classes" :key="classe.id" :value="classe.id">
                {{ classe.nom }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="fichier">Fichier :</label>
            <input type="file" id="fichier" @change="onFileChange" />
          </div>
          <button type="submit" class="btn-submit">Déposer</button>
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
        },
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
  .exercices-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .form-container {
    margin-bottom: 40px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  input[type="text"],
  textarea,
  select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  textarea {
    resize: vertical;
    min-height: 100px;
  }
  
  .btn-submit {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn-submit:hover {
    background-color: #45a049;
  }
  
  .liste-exercices {
    margin-top: 40px;
  }
  
  .exercice-item {
    background-color: #f9f9f9;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-bottom: 20px;
  }
  
  .exercice-item h3 {
    margin-top: 0;
  }
  
  .exercice-item a {
    color: #007bff;
    text-decoration: none;
  }
  
  .exercice-item a:hover {
    text-decoration: underline;
  }
  </style>