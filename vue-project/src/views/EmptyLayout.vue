<template>
    <div>
      <slot></slot> <!-- Le contenu de la route sera injecté ici -->
    
      <div id="navbar" class="bg-slate-800 text-white flex justify-between items-center flex-wrap p-2 px-6 rounded-lg">
   <!-- Le logo du site -->
  <div class="text-2xl">
    <a href="index.html">SMFCoder</a>
  </div>

 <!-- Le bloc hamburger caché -->
  <div class="block md:hidden">
    <label id="nav-toggle" for="toggleNavbar" class="flex gap-1 p-2 px-4 border border-current rounded-lg cursor-pointer select-none text-white">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 " fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7">
        </path>
      </svg>
      Menu
    </label>
  </div>

<input type="checkbox" name="" id="toggleNavbar" class="peer hidden">

<!-- NAV items -->
<ul class="text-xl md:text-lg my-5 md:my-0 h-0 w-full md:w-auto md:h-fit overflow-hidden peer-checked:h-fit absolute md:relative peer-checked:relative flex gap-3 items-center md:justify-center md:peer-checked:items-center justify-stretch peer-checked:flex-grow peer-checked:flex-col md:peer-checked:flex-row md:peer-checked:flex-grow-0  opacity-0 md:opacity-100 peer-checked:opacity-100 transition duration-300 peer-checked:translate-y-2 md:peer-checked:translate-y-0">
  <li class="py-2 px-4 rounded-lg text-center hover:bg-blue-500">Home</li>
  <li class="py-2 px-4 rounded-lg text-center hover:bg-blue-500">About</li>
  <li class="py-2 px-4 rounded-lg text-center hover:bg-blue-500">Services</li>
  <li class="py-2 px-4 rounded-lg text-center hover:bg-blue-500">Contact</li>
</ul>
</div>
    
    
    
    </div>
  </template>
  
  <script>
  export default {
    name: 'EmptyLayout',
  };
  </script>
  
  <style scoped>
  /* Styles spécifiques à ce layout */
  </style>


<div class="flex space-x-4">
  <router-link to="/dashboard-etudiant" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
    Tableau de bord
  </router-link>
  <router-link to="/exercices" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
    Exercices
  </router-link>
  <router-link to="/donnees" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
    Données
  </router-link>
  <router-link to="/profil" class="text-black hover:text-blue-400" active-class="text-red-500 underline underline-offset-8">
    Profil
  </router-link>
</div>