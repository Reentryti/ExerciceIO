<template>
  <div>
    <h1>Tableau de bord professeur</h1>
    <section>
      <h2>Mes exercices</h2>
      <ul>
        <li v-for="exercice in exercices" :key="exercice.id">
          <router-link :to="`/exercice/${exercice.id}`">{{ exercice.titre }}</router-link>
          (Date limite : {{ exercice.date_limite }})
        </li>
      </ul>
      <router-link to="/creation-exercice">Créer un nouvel exercice</router-link>
    </section>
    <section>
      <h2>Statistiques globales</h2>
      <p>Nombre total de soumissions : {{ total_soumissions }}</p>
      <p>Taux de réussite : {{ taux_reussite }}%</p>
      <div id="graphique-statistiques"></div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'DashboardProfesseur',
  data() {
    return {
      exercices: [],  // Liste des exercices créés par le professeur (à récupérer via une API)
      total_soumissions: 0,  // Nombre total de soumissions (à récupérer via une API)
      taux_reussite: 0,  // Taux de réussite (à calculer ou récupérer via une API)
    };
  },
  created() {
    // Récupérer les données (exercices, soumissions, etc.) via une API
    this.chargerDonnees();
  },
  methods: {
    chargerDonnees() {
      // Logique pour charger les données (appel API, etc.)
      console.log('Chargement des données pour le tableau de bord professeur...');
    },
  },
};
</script>

<style scoped>
/* Styles spécifiques au tableau de bord professeur */
</style>