import { createRouter, createWebHistory } from 'vue-router';
import Accueil from '../views/Accueil.vue';
import Connexion from '../views/Connexion.vue';
import Inscription from '../views/Inscription.vue';
import DashboardEtudiant from '../views/DashboardEtudiant.vue';
import DashboardProfesseur from '../views/DashboardProfesseur.vue';
import Exercices from '../views/Exercices.vue';  

const routes = [
    { path: '/', component: Accueil },
    { path: '/connexion', component: Connexion, name:'Login'},
    { path: '/inscription', component: Inscription },
    { path: '/dashboard-etudiant', component: DashboardEtudiant, name:'DashboardEtudiant',meta:{
        requiresAuth:true},
    },
    { path: '/dashboard-professeur', component: DashboardProfesseur, name:'DashboardProfesseur', meta:{
        requiresAuth:true},
    },
    { path: '/exercices', component: Exercices, meta:{
        requiresAuth:true},
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

//Securiser les routes
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token');
    if(to.meta.requiresAuth && !token){
        next({name:'Login'});
    } else{
        next();
    }
});

export default router;