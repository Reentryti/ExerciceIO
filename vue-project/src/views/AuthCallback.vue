<template>
  <div class="flex justify-center items-center h-screen">
    <div class="text-center p-8 bg-white rounded-lg shadow-lg max-w-md w-full">
      <!-- Étape de chargement initial -->
      <div v-if="loading">
        <h2 class="text-2xl font-bold mb-4">Authentification en cours...</h2>
        <div class="spinner-border animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
        <p class="mt-4 text-gray-600">Veuillez patienter pendant que nous terminons votre authentification.</p>
      </div>
      
      <!-- Étape de sélection de classe -->
      <div v-else-if="authSuccess && userRole === 'etudiant' && !classeSelected && !hasClasse">
        <h2 class="text-2xl font-bold mb-4">Bienvenue {{ userEmail }} !</h2>
        <p class="mb-4 text-gray-600">Veuillez sélectionner votre classe pour continuer :</p>
        
        <div v-if="loadingClasses">
          <p>Chargement des classes...</p>
          <div class="spinner-border animate-spin h-6 w-6 border-2 border-blue-500 border-t-transparent rounded-full mx-auto mt-2"></div>
        </div>
        
        <div v-else-if="classes.length === 0">
          <p class="text-red-500">Aucune classe disponible. Veuillez contacter un administrateur.</p>
        </div>
        
        <div v-else class="mt-4">
          <select 
            v-model="selectedClasse" 
            class="w-full p-2 border border-gray-300 rounded mb-4 focus:border-blue-500 focus:ring focus:ring-blue-200"
          >
            <option disabled value="">Sélectionnez une classe</option>
            <option v-for="classe in classes" :key="classe.id" :value="classe.id">
              {{ classe.nom }}
            </option>
          </select>
          
          <button 
            @click="confirmClasse" 
            class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded w-full"
            :disabled="!selectedClasse"
          >
            Continuer
          </button>
        </div>
      </div>
      
      <!-- Message d'erreur -->
      <div v-else-if="errorMessage">
        <h2 class="text-xl font-bold mb-4 text-red-500">Erreur d'authentification</h2>
        <p class="text-gray-700">{{ errorMessage }}</p>
        <button 
          @click="redirectToLogin" 
          class="mt-4 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
        >
          Retour à la connexion
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default{
  name: 'GoogleCallback',
  setup() {
    const router = useRouter();
    const loading = ref(true);
    const errorMessage = ref('');
    const authSuccess = ref(false);
    const userEmail = ref('');
    const userRole = ref('');
    const userToken = ref('');
    const userId = ref('');
    const classeSelected = ref(false);
    const selectedClasse = ref('');
    const classes = ref([]);
    const loadingClasses = ref(false);
    const hasClasse = ref(false);
    
    onMounted(() => {
      handleAuthCallback();
    });
    
    const handleAuthCallback = () => {
      //Paramètres de l'URL
      const urlParams = new URLSearchParams(window.location.search);
      const token = urlParams.get('token');
      const email = urlParams.get('email');
      const role = urlParams.get('role');
      const error = urlParams.get('error');
      const user_id = urlParams.get('user_id');
      
      console.log("URL params:", { token, email, role, error, user_id });
      
      if (error){
        errorMessage.value = `Erreur d'authentification: ${error}`;
        loading.value = false;
        return;
      }
      
      if (!token || !email){
        errorMessage.value = "Informations d'authentification incompletes";
        loading.value = false;
        return;
      }
      
      userToken.value = token;
      userEmail.value = email;
      userRole.value = role || 'etudiant';
      userId.value = user_id;
      
      const cleanUrl = window.location.origin + window.location.pathname;
      window.history.replaceState({}, document.title, cleanUrl);
      
      //Authentification réussie
      authSuccess.value = true;
      
      //Verification de la classe
      checkUserClass();
    };
    
    const checkUserClass = async() => {
      try{
        const config = {
          headers : {
            'Authorization': `Token ${userToken.value}`
          }
        };

        const response = await axios.get('http://localhost:8000/api/user/', config);
        
        //Log
        console.log("Réponse de l'API :", response.data);

        // Vérifier correctement si l'utilisateur a une classe
        if(response.data.user && response.data.user.classe !== null) {
          console.log("L'utilisateur a déjà une classe", response.data.user.classe);
          hasClasse.value = true;
          finalizeAuthentication();
        } else {
          console.log("L'utilisateur n'a pas de classe");
          loadClasses();
        }
        
        loading.value = false;
      } catch(error) {
        console.error("Erreur lors de la vérification du profil", error);
        errorMessage.value = "Impossible de vérifier le profil";
        loading.value = false;
      }
    };

    const loadClasses = async () => {
      loadingClasses.value = true;
      try{
        const config = {
          headers: {
            'Authorization': `Token ${userToken.value}`
          }
        };
        
        //Recuperation des classes
        const response = await axios.get('http://localhost:8000/api/classes/', config);
        classes.value = response.data;
        loadingClasses.value = false;
      } catch (error){
        console.error("Erreur lors du chargement des classes:", error);
        errorMessage.value = "Impossible de charger les classes. Veuillez réessayer.";
        loadingClasses.value = false;
      }
    };
    
    const confirmClasse = async () => {
      if(!selectedClasse.value) return;
      
      try{
        //Authentification parametres
        const config = {
          headers: {
            'Authorization': `Token ${userToken.value}`
          }
        };
        
        //Log
        console.log("Envoi des données:", { classe_id: selectedClasse.value });
      
        const response = await axios.post('http://localhost:8000/api/assign-classe/', 
          { classe_id: selectedClasse.value },
          config
        );
        
        console.log("Réponse assign-classe:", response.data);
        
        classeSelected.value = true;
        finalizeAuthentication();
      } catch(error) {
        console.error("Erreur lors de la mise à jour de la classe:", error.response?.data || error.message);
        //Redirection
        if(error.response?.data.error === "Vous avez une classe"){
          console.log("Utilisateur a deja une classe");
          hasClasse.value = true;
          finalizeAuthentication();
        }else{
        errorMessage.value = error.response?.data?.error || "Impossible d'associer la classe à votre compte. Veuillez réessayer.";
        }
      }
    };
    
    const finalizeAuthentication = () => {
      //Stockage des informations
      localStorage.setItem('token', userToken.value);
      localStorage.setItem('email', userEmail.value);
      localStorage.setItem('role', userRole.value);
      localStorage.setItem('user_id', userId.value);
      
      //Redirection
      if (userRole.value === 'professeur') {
        router.push({ name: 'DashboardProfesseur' });
      } else {
        router.push({ name: 'DashboardEtudiant' });
      }
    };
    
    const redirectToLogin = () => {
      router.push('/connexion');
    };
    
    return {
      loading,
      errorMessage,
      authSuccess,
      userEmail,
      userRole,
      classeSelected,
      selectedClasse,
      classes,
      loadingClasses,
      confirmClasse,
      redirectToLogin,
      hasClasse
    };
  }
};
</script>