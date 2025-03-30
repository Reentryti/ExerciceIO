import { createRouter, createWebHistory } from 'vue-router';
import Accueil from '../views/Accueil.vue';
import Home from '../views/Home.vue';
import Connexion from '../views/Connexion.vue';
import ConnexionProf from '../views/ConnexionProf.vue';
import Inscription from '../views/Inscription.vue';
import DashboardEtudiant from '../views/DashboardEtudiant.vue';
import DashboardProfesseur from '../views/DashboardProfesseur.vue';
import Profil from '../views/Profil.vue';
import Exercices from '../views/Exercices.vue';  
import Data from '../views/Data.vue';
import Correction from '../views/Correction.vue';
import Test from '../views/Dash.vue';
import AddExercice from '../views/Exercice.vue';
import ExerciceComposant from '../views/ExerciceComposant.vue';


const routes = [
    //{ path: '/', component: Accueil },
    { path: '/', component: Accueil, name:'Accueil'},
    { path: '/connexion', component: Connexion, name:'Login'},
    { path: '/connexion-professeur', component: ConnexionProf, name:'LoginProf'},
    { path: '/inscription', component: Inscription, name:'SignIn' },
    { path: '/dashboard-etudiant', component: DashboardEtudiant, name:'DashboardEtudiant',meta:{requiresAuth:true},},
    { path: '/dashboard-professeur', component: DashboardProfesseur, name:'DashboardProfesseur', meta:{requiresAuth:true},},
    { path: '/exercices', component: Exercices, meta:{requiresAuth:true},},
    { path: '/add-exercice', component : AddExercice, meta:{requiresAuth:true},},
    { path: '/exercice/:id', component: ExerciceComposant, name:'ExerciceComposant' , meta:{requiresAuth:true}},
    { path: '/profil', component: Profil, meta:{requiresAuth:true},},
    { path: '/donnees', component: Data, name:'Data', meta:{requiresAuth:true},},
    { path: '/correction', component: Correction, name:'Correction', meta:{requiresAuth:true},},
    { path: '/dash', component: Test, name:'Dash', meta:{requiresAuth:true},},
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