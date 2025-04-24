<template>
  <div class="flex justify-center items-center h-screen">
    <div class="text-center p-8 bg-white rounded-lg shadow-lg">
      <h2 class="text-2xl font-bold mb-4">Authentification en cours...</h2>
      <div v-if="loading" class="spinner-border animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
      <div v-else>
        <p>Token: {{ params.token || 'Manquant' }}</p>
        <p>Email: {{ params.email || 'Manquant' }}</p>
        <p>Role: {{ params.role || 'Manquant' }}</p>
        <p>Error: {{ params.error || 'Aucune' }}</p>
        <button @click="continueToApp" class="mt-4 bg-blue-500 text-white px-4 py-2 rounded">Continuer</button>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'GoogleCallback',
  setup() {
    const router = useRouter();
    const loading = ref(true);
    const params = ref({});
    
    onMounted(() => {
      const urlParams = new URLSearchParams(window.location.search);
      params.value = {
        token: urlParams.get('token'),
        email: urlParams.get('email'),
        role: urlParams.get('role'),
        error: urlParams.get('error')
      };
      
      console.log("URL params:", params.value);
      console.log("Full URL:", window.location.href);
      
      loading.value = false;
    });
    
    const continueToApp = () => {
      if (params.value.token && params.value.email) {
        localStorage.setItem('token', params.value.token);
        localStorage.setItem('email', params.value.email);
        localStorage.setItem('role', params.value.role || 'etudiant');
        
        if ((params.value.role || 'etudiant') === 'professeur') {
          router.push({ name: 'DashboardProfesseur' });
        } else {
          router.push({ name: 'DashboardEtudiant' });
        }
      } else {
        alert("Informations d'authentification incomplètes");
        router.push('/connexion');
      }
    };
    
    return { loading, params, continueToApp };
  }
};
</script>