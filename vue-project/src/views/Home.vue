<template>
  <div class="min-h-screen">
    <!-- En-tête -->
    <header class="p-6 flex justify-between items-center">
      <!-- Logo de la plateforme -->
      <div class="text-2xl font-bold text-blue-800">
        <img src="../../public/images/icone.png" alt="Logo de la plateforme" class="h-12" />
      </div>

      <!-- Boutons de connexion -->
      <div class="flex space-x-4">
        <button
          @click="redirectToTeacherLogin"
          class="bg-inherit text-black hover:text-red-500 px-6 py-2 rounded-lg hover:text-gray-400 transition-colors duration-300"
          aria-label="Je suis professeur"
        >
          Je suis professeur
        </button>
        <button
          @click="redirectToStudentLogin"
          class="bg-inherit border-1 text-black hover:text-red-500 px-6 py-2 rounded-lg hover:text-gray-400 transition-colors duration-300"
          aria-label="Je suis étudiant"
        >
          Je suis étudiant
        </button>
      </div>
    </header>

    <!-- Contenu principal -->
    <main class="container mx-auto px-6 py-12">
      <!-- Phrase d'accroche -->
      <section class="text-center mb-16">
        <h1 class="text-5xl font-bold text-black mb-4">
          Plateforme d'exercices de bases de données automatisée avec l'IA
        </h1>
        <p class="text-xl text-black">
          Apprenez, enseignez et évaluez de manière intelligente et efficace.
        </p>
      </section>

      <!-- Bloc pour la fonction étudiant -->
      <section class="bg-[#030712] p-8 rounded-lg shadow-lg mb-8">
        <h2 class="text-3xl font-bold text-blue-800 mb-4">Dashboard Étudiant</h2>
        <p class="text-gray-700 mb-4">
          En tant qu'étudiant, accédez à des exercices personnalisés, recevez des corrections instantanées et progressez à votre rythme grâce à l'IA.
        </p>
        <router-link to="/dashboard-etudiant" class="hover:underline transition-all duration-500">
          En savoir plus >
        </router-link>
      </section>

      <!-- Bloc pour la fonction professeur -->
      <section class="bg-white p-8 rounded-lg shadow-lg mb-8">
        <h2 class="text-3xl font-bold text-purple-800 mb-4">Fonction Professeur</h2>
        <p class="text-gray-700 mb-4">
          En tant que professeur, créez des exercices, suivez les progrès de vos étudiants et bénéficiez de corrections automatisées pour gagner du temps.
        </p>
        <router-link to="/dashboard-professeur" class="hover:underline transition-all duration-500">
          En savoir plus >
        </router-link>
      </section>

      <!-- Bloc pour les corrections automatisées -->
      <section class="bg-white p-8 rounded-lg shadow-lg">
        <h2 class="text-3xl font-bold text-green-800 mb-4">Corrections Automatisées</h2>
        <p class="text-gray-700 mb-4">
          Grâce à l'intelligence artificielle, les corrections sont instantanées, précises et adaptées à chaque étudiant.
        </p>
        <router-link to="/corrections" class="hover:underline transition-all duration-500">
          En savoir plus >
        </router-link>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: 'Home',
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('token');
    },
  },
  mounted() {
    if (!this.isAuthenticated) {
      this.$router.push('/connexion');
    }
  },
  methods: {
    redirectToStudentLogin() {
      this.$router.push('/connexion'); 
    },
    redirectToTeacherLogin() {
      this.$router.push('/connexion-professeur');
    },
  },
};
</script>

<style scoped>
/* Styles spécifiques à cette vue */
#app{
  background-color: #030712;
}
</style>