import { createRouter, createWebHistory } from 'vue-router';
import Accueil from '../views/Accueil.vue';
import Connexion from '../views/Connexion.vue';
import Inscription from '../views/Inscription.vue';
import DashboardEtudiant from '../views/DashboardEtudiant.vue';
import DashboardProfesseur from '../views/DashboardProfesseur.vue';

const routes = [
    { path: '/', component: Accueil },
    { path: '/connexion', component: Connexion },
    { path: '/inscription', component: Inscription },
    { path: '/dashboard-etudiant', component: DashboardEtudiant },
    { path: '/dashboard-professeur', component: DashboardProfesseur },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;