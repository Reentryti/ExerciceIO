<template>
  <div class="items-center justify-items-center mt-10">
    
    <!-- Block principal -->
    <div class="grid grid-cols-1 md:grid-cols-2 w-full max-w-4xl bg-white rounded-lg shadow-lg overflow-hidden">
      
      <!-- Partie Formulaire d'inscription -->
      <div class=" p-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-6">Inscription</h2>
        <form @submit.prevent="sInscrire">
          <div class="flex flex-wrap -mx-3 mb-6">
            <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
              <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                Prénom
              </label>
              <input name="prenom" v-model="prenom" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="grid-first-name" type="text" required/>
            </div>
            <div class="w-full md:w-1/2 px-3">
              <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-last-name">
                Nom
              </label>
              <input name="nom" v-model="nom" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="grid-last-name" type="text" required/>
            </div>
          </div>

          <div class="flex flex-wrap -mx-3 mb-6">
            <div class="w-full px-3">
              <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-email">
                Email
              </label>
              <input name="email" v-model="email" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="grid-email" type="email" required/>
            </div>
          </div>

          <div class="flex flex-wrap -mx-3 mb-6">
            <div class="w-full px-3">
              <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-password">
                Mot de passe
              </label>
              <input
                name="password"
                v-model="password" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="grid-password" type="password" required/>
            </div>
          </div>

          <div class="flex flex-wrap -mx-3 mb-6">
            <div class="w-full px-3">
              <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-classe">
                Classe
              </label>
              <select v-model="classe" class="block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="grid-classe" required>
                <option v-for="classe in classes" :key="classe.id" :value="classe.id">
                  {{ classe.nom }}
                </option>
              </select>
            </div>
          </div>

          <div class="flex items-center justify-between">
            <button
              class="mb-5 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="submit">
              S'inscrire
            </button>
          </div>
        </form>
      </div>

      <!-- Partie droite : Message et bouton de redirection -->
      <div class="bg-[#0f172b] text-white p-8 flex flex-col items-center justify-center">
        <h3 class="text-2xl font-bold mb-4">Déjà un compte ?</h3>
        <p class="text-center mb-6">
          Connectez-vous pour accéder à votre espace personnel.
        </p>
        <router-link to="/connexion" class="bg-white text-black hover:text-white hover:bg-blue-800 font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
          Se connecter
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Inscription',
  data() {
    return {
      prenom: '',
      nom: '',
      email: '',
      password: '',
      classe: '',  // ID de la classe sélectionnée
      role: 'etudiant',  // Définir 'etudiant' par défaut
      classes: [],  // Liste des classes récupérées depuis l'API
    };
  },
  created() {
    this.reloadClasses();  // Charge les classes au moment de la création du composant
  },
  methods: {
    async reloadClasses() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/classes/');  // Appel à l'API Django
        this.classes = response.data;  // Stocke les classes dans la variable `classes`
      } catch (error) {
        console.error('Erreur lors du chargement des classes:', error);
      }
    },
    async sInscrire() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/register/', {
          prenom: this.prenom,
          nom: this.nom,
          email: this.email,
          password: this.password,
          classe: this.classe,  // Envoi de l'ID de la classe sélectionnée
          role: this.role,
        });

        console.log('Inscription réussie:', response.data);
        alert('Inscription réussie !');
        this.$router.push('/connexion');  // Redirige vers la page de connexion après inscription
      } catch (error) {
        console.error('Erreur lors de l’inscription:', error.response?.data || error.message);
        alert('Erreur lors de l’inscription. Veuillez réessayer.');
      }
    },
  },
};
</script>

<style scoped>
/* Styles spécifiques à la page d'inscription */
#app{
  display: none;
}
</style>