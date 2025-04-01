<template>
    <div class="">
      <div class=" mx-auto">
  
        <!-- Grille pour les graphiques -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Graphique 1 : Notes par exercice -->
          <div class="bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-xl font-semibold text-gray-700 mb-4">
              Notes par exercice
            </h2>
            <div v-if="loading" class="text-center py-8">
              Chargement des données ...
            </div>
            <canvas v-else ref="gradesChart"></canvas>
          </div>
  
          <!-- Graphique 2 : Progression globale -->
          <div class="bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-xl font-semibold text-gray-700 mb-4">
              Progression globale
            </h2>
            <div v-if="loading" class="text-center py-8">
              Chargement des données ...
            </div>
            <canvas v-else ref="progressChart"></canvas>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { Chart, registerables } from 'chart.js';
  import axios from 'axios';
  
  // Enregistrer les composants nécessaires de Chart.js
  Chart.register(...registerables);
  
  export default {
    setup() {
      const gradesChart = ref(null);
      const progressChart = ref(null);
      const exercices = ref([]);
      const solutions = ref([]);
      const loading = ref(true);
  
      const fetchData = async() =>{
        try{
          const token = localStorage.getItem('token');

          const exerciceResponse = await axios.get('/exercices/liste/',{
            headers: {
              "Authorization": `Token ${token}`
            }
          });
          exercices.value = exerciceResponse.data;

          const solutionsResponse = await axios.get('/exercices/',{
            headers: {
              "Authorization": `Token ${token}`
            }
          });
          solutions.value = solutionsResponse.data;

          //Creation du graphique en fonction des données récupérées
          createCharts();
        } catch(error){
          console.error('Erreur de récupération des données:', error);
        } finally{
          loading.value = false;
        }
      };

      const createCharts = () => {
        const exerciceNote= {};
        solutions.value.forEach(solution =>{
          if(solution.note && solution.exercice){
            const exerciceID = solution.exercice;
            const exercice = exercices.value.find(e=>e.id === exerciceID);

            if(exercice){
              exerciceNote[exercice.titre] = solution.note;
            }
          }
        });

        //Graphe des notes d'exercices
        new Chart(gradesChart.value,{
          type:'bar',
          data:{
            labels:Object.keys(exerciceNote),
            datasets:[{
              label:'Notes',
              data:Object.values(exerciceNote),
              backgroundColor:'rbga()',
              borderColor:'rgba()',
              borderWidth:1
            }]
          },
          options:{
            scales:{
              y:{
                beginAtZero:true,
                max:20,
                title:{
                  display:true,
                  text:'Note /20'
                }
              }
            }
          }
        });

        //Graphe de progression
        const progressionData = [];
        let cumuleNote = 0;

        solutions.value.sort((a,b) => new Date(a.date_a_soumettre) - new Date(date_a_soumettre)).forEach((solution, index) => {
          if(solution.note){
            cumuleNote+= solution.note;
            progressionData.push({
              label:`Ex. ${index + 1}`,
              value:cumuleNote / (index + 1) //Moyenne
            });
          }
        });


        new Chart(progressChart.value,{
          type:'line',
          data:{
            labels: progressionData.map(item=>item.label),
            datasets:[{
              label:'Moyenne',
              data:progressionData.map(item=>item.value),
              fill:true,
              backgroundColor:'rgba()',
              borderColor:'rgba()',
              borderWidth: 2,
              tension:0.1
            }]
          },
          options:{
            scales: {
              y:{
                beginAtZero: true,
                max:20,
                title:{
                  display:true,
                  text:'Moyenne /20'
                }
              }
            }
          }
        });
      };
  
      return {
        gradesChart,
        progressChart,
        loading
      };
    }
  };
  </script>
  
  <style scoped>
  /* Styles spécifiques à cette vue */
  </style>