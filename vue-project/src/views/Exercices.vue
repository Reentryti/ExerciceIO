<template>
  <!-- Bloc de bienvenue -->
  <div class="bg-gradient-to-b from-white via-white to-red-100 h-72 mx-w-md overflow-hidden mx-5 md:mx-20 mb-7">
    <div class="text-left mx-auto pl-20">
      <div>
        <p class="text-black tracking-wide text-6xl md:text-5xl font-bold text-gray-800 mb-10 mt-auto">
          Exercices
        </p>
      </div>
    </div>
  </div>

  <!-- Bloc des exercices -->
  <div class=" flex flex-col gap-10 md:flex-row-reverse mx-5 md:mx-20">
    
    <!-- Sous-bloc des exercices -->
    <div class="grid grid-col-1 w-full border border-gray-300 rounded-lg md:w-2/3">
      <div class="flex flex-row ">
        <div class="flex flex-col gap-2 p-8 sm:flex-row sm:items-center sm:gap-6 sm:py-4 ...">
          <div class="space-y-2 text-center sm:text-left">
            <div class="space-y-0.5">
              <p class="text-lg font-semibold text-black">
                Nom du professeur
              </p>
              <p class="font-medium text-gray-500">
                Description de l'exercice
              </p>
            </div>
            <button class="border-purple-200 text-purple-600 hover:border-transparent hover:bg-purple-600 hover:text-white active:bg-purple-700 ...">
              Message
            </button>
          </div>
        </div>
        <div></div>
      </div>

    </div>


     <!-- Sous-bloc des corrigés -->
    <div class="hidden md:inline border border-gray-300 rounded w-1/3 ">
      Partie corrections
      <ul role="list" class="divide-y divide-gray-100">
        <li v-for="person in people" :key="person.email" class="flex justify-between gap-x-6 py-5">
          <div class="flex min-w-0 gap-x-4">
            <div class="min-w-0 flex-auto">
              <p class="text-sm/6 font-semibold text-gray-900">{{ person.name }}</p>
              <p class="mt-1 truncate text-xs/5 text-gray-500">{{ person.email }}</p>
            </div>
          </div>
          <div class="hidden shrink-0 sm:flex sm:flex-col sm:items-end">
            <p class="text-sm/6 text-gray-900">{{ person.role }}</p>
            <p v-if="person.lastSeen" class="mt-1 text-xs/5 text-gray-500">
              Last seen <time :datetime="person.lastSeenDateTime">{{ person.lastSeen }}</time>
            </p>
            <div v-else class="mt-1 flex items-center gap-x-1.5">
              <div class="flex-none rounded-full bg-emerald-500/20 p-1">
                <div class="size-1.5 rounded-full bg-emerald-500" />
              </div>
              <p class="text-xs/5 text-gray-500">Online</p>
            </div>
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