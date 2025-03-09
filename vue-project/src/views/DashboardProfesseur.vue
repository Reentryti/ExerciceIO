<template>
    <!--This example requires updating your template:
   ```
    <html class="h-full bg-gray-100">
    <body class="h-full">
    ```
  -->
  <div class="min-h-full">

    <header class="bg-white shadow-sm">
      <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold tracking-tight text-gray-900">Dashboard</h1>
      </div>
    </header>
    <main>
      <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <!-- Your content -->
      </div>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // Données des classes
      classes: [
        {
          id: 1,
          name: "Licence 1",
          description: "Classe licence génie logiciel",
        },
        {
          id: 2,
          name: "Master IABD",
          description: "Classe master jour iabdb",
        },
        {
          id: 3,
          name: "Master GLSI",
          description: "Classe master soir glsi",
        },
      ],
    };
  },
  methods: {
    // Méthode pour accéder à une classe spécifique
    viewClass(classId) {
      // Redirection vers la page de la classe (à implémenter)
      console.log("Accéder à la classe avec l'ID :", classId);
      this.$router.push({ name: "ClassDetails", params: { id: classId } });
    },
  },
};
</script>

<style scoped>
/* Styles spécifiques à cette vue */
</style>