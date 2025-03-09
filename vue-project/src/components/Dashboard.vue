<template>
  <div>
    <h2>Welcome to your Dashboard</h2>
    <p v-if="isProfesseur">You are a Professor</p>
    <p v-else>You are a Student</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isProfesseur: false
    };
  },
  mounted() {
    // Vérifie le type d'utilisateur et affiche le dashboard correspondant
    const token = localStorage.getItem('token');
    if (token) {
      this.isProfesseur = true;  // Tu peux récupérer cette info via une API ou une variable d'état
    }
  }
};
</script>
