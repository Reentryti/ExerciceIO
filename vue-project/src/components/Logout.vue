// src/components/Logout.vue
<template>
  <button @click="logout">Se déconnecter</button>
</template>

<script>
export default {
  methods: {
    logout() {
      localStorage.removeItem('token');  // Supprimer le token
      this.$router.push({ name: 'Login' });  // Rediriger vers la page de connexion
    },
  },
};
</script>