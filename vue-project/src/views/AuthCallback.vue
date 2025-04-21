<template>
  <div class="flex justify-center items-center h-screen">
    <div class="text-center p-8 bg-white rounded-lg shadow-lg">
      <h2 class="text-2xl font-bold mb-4">Authentification en cours...</h2>
      <div class="spinner-border animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
      <p class="mt-4 text-gray-600">Veuillez patienter pendant que nous terminons votre authentification.</p>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'GoogleCallback',
  setup() {
    const router = useRouter();

    onMounted(() => {
      handleCallback();
    });

    const handleCallback = () => {
      // Récupérer les paramètres de l'URL
      const urlParams = new URLSearchParams(window.location.search);
      const token = urlParams.get('token');
      const email = urlParams.get('email');
      const role = urlParams.get('role');
      const error = urlParams.get('error');

      if (error) {
        alert(`Erreur d'authentification: ${error}`);
        router.push('/login');
        return;
      }

      if (token && email && role) {
        // Stocker les informations de l'utilisateur
        localStorage.setItem('token', token);
        localStorage.setItem('email', email);
        localStorage.setItem('role', role);

        // Nettoyer l'URL
        const cleanUrl = window.location.origin + window.location.pathname;
        window.history.replaceState({}, document.title, cleanUrl);

        // Rediriger vers le tableau de bord approprié
        if (role === 'professeur') {
          router.push({ name: 'DashboardProfesseur' });
        } else {
          router.push({ name: 'DashboardEtudiant' });
        }
      } else {
        // En cas d'erreur ou d'informations manquantes
        alert("Échec de l'authentification. Veuillez réessayer.");
        router.push('/login');
      }
    };

    return {};
  }
};
</script>