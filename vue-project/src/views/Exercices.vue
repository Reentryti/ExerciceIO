<template>
  <!-- Bloc de bienvenue -->
  <div class="bg-gradient-to-b from-white via-white to-blue-200 h-72 mx-w-md overflow-hidden ">
    <div class="text-left mx-auto">
      <div>
        <p class="text-black font-bold tracking-wide text-6xl">
          Exercices
        </p>
        <p class="text-white">
          Bases de données
        </p>
      </div>
    </div>
  </div>

  <!-- Bloc des exercices -->
  <div class="border flex flex-row-reverse gap-10">
    
    <!-- Sous-bloc des exercices -->
    <div class="grid grid-col-1 w-2/3">
      <div class="flex flex-row">
        <div class="border rounded-s-xl w-1/5">
          <p>
            Note attribuée
          </p>
        </div>
        <div class="border w-4/5 overflow-hidden">
          <p>
            Nom de l'exercice
          </p>
        </div>
      </div>

    </div>


     <!-- Sous-bloc des corrigés -->
    <div class="border w-1/3">
      Partie corrections
      <ul role="list">
        <li class="flex py-4 ">
          <div class="ml-8 overflow-hidden">
            <p class=""></p>
            <p class=""></p>
          </div>
        </li>
      </ul>
    </div>
  </div>


  <!-- Bloc de pagination -->
</template>
  
<script>
  
</script>
  
<style scoped>
/* Styles spécifiques au dashboard */
</style>