<template>
  <!--
    This example requires updating your template:

    ```
    <html class="h-full bg-white">
    <body class="h-full">
    ```
  -->
  <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <img class="mx-auto h-15 w-auto" src="../../public/logo.png" alt="Your Company" />
      <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">Compte Enseignant</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <form class="space-y-6" action="#" method="POST">
        <div>
          <label for="email" class="block text-sm/6 font-medium text-gray-900">Adresse email</label>
          <div class="mt-2">
            <input type="email" name="email" id="email" autocomplete="email" required="" class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-600 sm:text-sm/6" />
          </div>
        </div>

        <div>
          <div class="flex items-center justify-between">
            <label for="password" class="block text-sm/6 font-medium text-gray-900">Mot de passe</label>
            <div class="text-sm">
              <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-500">mot de passe oublié?</a>
            </div>
          </div>
          <div class="mt-2">
            <input type="password" name="password" id="password" autocomplete="" required="" class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6" />
          </div>
        </div>

        <div>
          <button type="submit" class="flex w-full justify-center rounded-md bg-blue-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-blue-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
            Se connecter
          </button>
        </div>
      </form>
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
            if (response.data.role === 'professeur') {
              this.$router.push({name:'DashboardProfesseur'});
            }
              
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