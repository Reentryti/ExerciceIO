<template>
<div class="min-h-screen bg-cover bg-center flex items-center justify-center p-6" >
    
    <!-- Main Connexion Container -->
    <div class="w-full max-w-4xl bg-white/0 rounded-lg shadow-lg overflow-hidden flex">
      
      <!-- Partie formulaire de connexion -->
      <div class="w-2/3 p-8">
        <h2 class="text-5xl font-bold text-blue-600 dark:text-sky-400 mb-6">Connexion</h2>
        <form @submit.prevent="seConnecter">
          <div class="mb-4">
            <label class="block text-3xl text-blue-600 font-bold mb-2" for="email">
              Email
            </label>
            <input
              v-model="email"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-blue-600 leading-tight focus:outline-none focus:shadow-outline"
              id="email"
              type="email"
              placeholder="Email"
              required
            />
          </div>
          <div class="mb-6">
            <label class="block text-3xl text-blue-600 font-bold mb-2" for="password">
              Mot de passe
            </label>
            <input
              v-model="password"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
              id="password"
              type="password"
              placeholder="******************"
              required
            />
          </div>
          <div class="flex items-center justify-between">
            <button
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="submit"
            >
              Se connecter
            </button>
          </div>
        </form>
      </div>

      <!-- Partie droite : Message et bouton de redirection -->
      <div class="w-1/3 bg-blue-500 text-white p-8 flex flex-col items-center justify-center">
        <h3 class="text-2xl font-bold mb-4">Pas encore de compte ?</h3>
        <p class="text-center mb-6">
          Inscrivez-vous pour accéder à votre espace personnel.
        </p>
        <router-link
          to="/inscription"
          class="bg-white text-blue-500 font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        >
          S'inscrire
        </router-link>
      </div>
    </div>
</div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'Connexion',
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    async seConnecter() {
      try {
        // Envoi de la requête de connexion à l'API Django
        const response = await axios.post('http://127.0.0.1:8000/api/login/', {
          email: this.email,
          password: this.password,
        });

        // Si la connexion est réussie
        console.log('Connexion réussie:', response.data);
        alert('Connexion réussie !');

        // Rediriger vers la page d'accueil ou un tableau de bord après connexion réussie
        this.$router.push('/');  // Redirige vers la page d'accueil (ou autre page)
      } catch (error) {
        console.error('Erreur lors de la connexion:', error.response?.data || error.message);
        alert('Erreur lors de la connexion. Vérifiez vos identifiants.');
      }
    },
  },
};
</script>

<style scoped>
/* Styles spécifiques à la page de connexion */
</style>