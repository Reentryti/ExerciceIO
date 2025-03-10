<template>
    <div class="justify-center items-center justify-items-center mt-10">
      <!-- Main Connexion Container -->
      <div class=" grid grid-cols-1 md:grid-cols-2  gap-12 rounded-lg shadow-2xl ">
        
        <!-- Partie formulaire de connexion -->
        <div class=" col-span-1 p-8 rounded-xl">
          <h2 class="text-5xl font-bold text-black mb-6 font-light">Connexion</h2>
          <form @submit.prevent="seConnecter">
            <div class="mb-4">
              <label class="block text-1xl text-white font-bold mb-2 font-light" for="email">
                Adresse Email
              </label>
              <input v-model="email" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-600 leading-tight focus:border-pink-100" id="email" type="email" required/>
            </div>
            <div class="mb-6">
              <label class="block text-1xl text-white font-bold mb-2 font-light" for="password">
                Mot de passe
              </label>
              <input v-model="password" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:border-blue-100 " id="password" type="password" required/>
              <div>
                <p>
                  J'ai oublié mon mot de passe
                </p>
              </div>
            </div>

            <div class="items-center justify-items-center justify-center shadow-2xl">
              <button class="w-full bg-[#0f172b] hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="submit">
                Se connecter
              </button>
            </div>
          </form>
  
          <!-- Boutons de connexion avec Google -->
          <div class="mt-6">
            <p class="text-center text-gray-600 mb-4">Ou connectez-vous avec</p>
            <button @click="connexionGoogle" class="w-full flex items-center justify-center bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
              <svg class="w-6 h-6 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 488 512">
                <path fill="currentColor" d="M488 261.8C488 403.3 391.1 504 248 504 110.8 504 0 393.2 0 256S110.8 8 248 8c66.8 0 123 24.5 166.3 64.9l-67.5 64.9C258.5 52.6 94.3 116.6 94.3 256c0 86.5 69.1 156.6 153.7 156.6 98.2 0 135-70.4 140.8-106.9H248v-85.3h236.1c2.3 12.7 3.9 24.9 3.9 41.4z"/>
              </svg>
              Google
            </button>
          </div>
        </div>
  
        <!-- Partie Redirection -->
        <div class="col-span-1 bg-[#0f172b] text-white p-8 items-center justify-center rounded-xl flex flex-col">
          <h3 class="text-2xl font-bold mb-10 mt-10">Pas encore de compte ?</h3>
          <p class="text-center mb-8">
            Inscrivez-vous pour accéder à votre espace personnel.
          </p>
          <router-link to="/inscription" class="bg-white text-black font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
            S'inscrire
          </router-link>
  
          <!-- Boutons d'inscription avec Google -->
          <div class="mt-6">
            <p class="text-center mb-4">Ou inscrivez-vous avec</p>
            <button @click="inscriptionGoogle" class="w-full flex items-center justify-center bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
              <svg class="w-6 h-6 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 488 512">
                <path fill="currentColor" d="M488 261.8C488 403.3 391.1 504 248 504 110.8 504 0 393.2 0 256S110.8 8 248 8c66.8 0 123 24.5 166.3 64.9l-67.5 64.9C258.5 52.6 94.3 116.6 94.3 256c0 86.5 69.1 156.6 153.7 156.6 98.2 0 135-70.4 140.8-106.9H248v-85.3h236.1c2.3 12.7 3.9 24.9 3.9 41.4z"/>
              </svg>
              Google
            </button>
          </div>
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
  
          // Afficher la réponse de l'API pour le débogage
          console.log('Réponse de l\'API:', response.data);
          
          //Recupération du token
          localStorage.setItem('token', response.data.token);
          //Recupération du role
          localStorage.setItem('role', response.data.role);
  
          console.log('Token:', localStorage.getItem('token'));
          console.log('Role:', localStorage.getItem('role'));
          // Si la connexion est réussie
          console.log('Connexion réussie:', response.data);
          alert('Connexion réussie !');
  
          //Redirection vers le tableau de bord en fonction du role
          if (response.data.role === 'etudiant') {
            this.$router.push({name:'DashboardEtudiant'});
          } else if(response.data.role === 'professeur') {
            this.$router.push({name:'DashboardProfesseur'});  
          }
            
        } catch (error) {
          console.error('Erreur lors de la connexion:', error.response?.data || error.message);
          alert('Erreur lors de la connexion. Vérifiez vos identifiants.');
        }
      },
  
      connexionGoogle() {
        // Redirection vers l'URL d'authentification Google
        window.location.href = 'http://127.0.0.1:8000/accounts/google/login/';
      },
  
      inscriptionGoogle() {
        // Redirection vers l'URL d'inscription Google
        window.location.href = 'http://127.0.0.1:8000/accounts/google/signup/';
      },
    },
  };
  </script>
  
  <style scoped>
  /* Styles spécifiques à la page de connexion */
  </style>