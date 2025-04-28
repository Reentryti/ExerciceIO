<template>
  <div class="min-h-screen p-8">
    <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-lg">
      <!-- Titre de la page -->
      <div class="flex flex-col rounded-t-lg h-40 md:h-72 w-full bg-linear-to-b from-blue-500 p-10">
        <h1 class="text-2xl md:text-5xl font-bold text-gray-800 mb-20 mt-auto">Profil Utilisateur</h1>
      </div>
      

      <!-- Section des informations utilisateur -->
      <div class="mt-8 space-y-6 p-8">
        <!-- Informations personnelles -->
        <div>
          <h2 class="text-xl font-semibold text-gray-700 mb-4">Informations personnelles</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-600">Prénom</label>
              <input type="text" :value="user.prenom"readonly class="mt-1 block w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-md shadow-sm"/>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-600">Nom</label>
              <input type="text" :value="user.nom" readonly class="mt-1 block w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-md shadow-sm"/>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-600">Email</label>
              <input type="email" :value="user.email" readonly class="mt-1 block w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-md shadow-sm"/>
            </div>
            <!-- Selecttion d'une classe -->
             <div v-if="!user.classe && classes && classes.length > 0">
              <label for="" class="block text-sm font-medium text-gray-600">
                Choisir une classe
              </label>
              <select v-model="selectedClasse" name="" id="" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-300">
                <option disabled value="">
                  Sélectionnez une classe
                </option>
                <option v-for="classe in classes" :key="classe.id" :value="classe.id"> 
                  {{ classe.nom }}
                </option>
              </select>
              <button @click="assignClasse" class="mt-2 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
                Valider la classse
              </button>
             </div>
             <div v-else-if="user.classe">
              <label for="" class="block text-sm font-medium text-gray-500">
                Classe
              </label>
              <input type="text" name="" id="" :value="user.classe.nom" readonly class="mt-1 block w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-md shadow-sm">
             </div>
          </div>
        </div>

        <!-- Section de changement de mot de passe -->
        <div class="pt-6 border-t border-gray-200">
          <h2 class="text-xl font-semibold text-gray-700 mb-4">Changer le mot de passe</h2>

          <!-- Ancien mot de passe -->
          <div class="mb-4">
            <label for="oldPassword" class="block text-sm font-medium text-gray-600">Ancien mot de passe</label>
            <input v-model="password.oldPassword" type="password" id="oldPassword" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500"/>
          </div>

          <!-- Nouveau mot de passe -->
          <div class="mb-4">
            <label for="newPassword" class="block text-sm font-medium text-gray-600">Nouveau mot de passe</label>
            <input v-model="password.newPassword" type="password" id="newPassword" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500"/>
          </div>

          <!-- Confirmation du nouveau mot de passe -->
          <div class="mb-6">
            <label for="confirmPassword" class="block text-sm font-medium text-gray-600">Confirmer le nouveau mot de passe</label>
            <input v-model="password.confirmPassword" type="password" id="confirmPassword" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500"/>
          </div>

          <!-- Bouton de soumission -->
          <button @click="changePassword" class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
            Changer le mot de passe
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
//import axios from 'axios';
import api from '@/utils/axios-inter';

export default {
  data(){
    return{
      //Données de l'utilisateur
      user:{
        prenom: "",
        nom: "",
        email: "",
        classe: null
      },
      //Données pour le changement de mot de passe
      password: {
        oldPassword: "",
        newPassword: "",
        confirmPassword: "",
      },
      classes : [], //Liste des classes dispo
      selectedClasse : "", //Classe selectionnée
      loading: true,
      error: false,
      errorMessage: ""//Message d'erreur
    };
  },
  methods: {
    //Récupérer les informations de l'utilisateur
    async fetchUser(){
      this.loading = true;
      this.error = false;
      try{
        const response = await axios.get("http://localhost:8000/api/user/", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.user = response.data;
        this.classes = response.data.classes || [];
      } catch (error) {
        console.error("Erreur lors de la récupération des informations utilisateur :", error);
        this.error = true;
        this.errorMessage = "Impossible de recuperer les informatinos ";
      }
      finally{
        this.loading = false;
      }
    },

    //Attribuer une classe
    async assignClasse(){
      if(!this.selectedClasse){
        alert("Veuillez selectionner une classe");
        return;
      }
      this.loading = true;
      try{

        await axios.post("http://localhost:8000/api/assign-class/",
          {
            classe_id: this.selectedClasse
          },
          {
            headers:{
              Authorization:`Bearer ${localStorage.getItem('token')}`,
            },
          }
        );
        alert("Classe attribué avec succés");
        this.fetchUser();
  
      }catch(error){
        console.error("Erreur lors de l'attribution de la classe:", error);
        alert("Une erreur s'est produite  lors de l'attribution de la classe");
      }finally{
        this.loading = false;
      }
    },

    // Changer le mot de passe
    async changePassword(){
      // Validation des champs
      if (this.password.newPassword !== this.password.confirmPassword) {
        alert("Les nouveaux mots de passe ne correspondent pas.");
        return;
      }
      if (!this.password.oldPassword) {
        alert("Veuillez renseigner votre ancien mot de passe.");
        return;
      }

      try {
        const response = await axios.post(
          "http://localhost:8000/api/change-password/",
          {
            old_password: this.password.oldPassword,
            new_password: this.password.newPassword,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          }
        );
        alert("Mot de passe changé avec succès !");
        this.password = { oldPassword: "", newPassword: "", confirmPassword: "" }; // Réinitialiser les champs
      } catch (error) {
        console.error("Erreur lors du changement de mot de passe :", error);
        alert("Une erreur s'est produite. Veuillez vérifier votre ancien mot de passe.");
      }
    },
  },
  mounted() {
    this.fetchUser(); // Récupérer les informations de l'utilisateur au chargement
  },
};
</script>

<style scoped>
/* Styles spécifiques à cette vue */
</style>