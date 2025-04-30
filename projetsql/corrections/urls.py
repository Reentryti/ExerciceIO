from django.urls import path
from .views import SoumettreCorrectionAPI, CorrigerSolutionAPI, CorrigerToutesSolutionsAPI

urlpatterns = [
    path('exercices/<int:exercice_id>/soumettre/', SoumettreCorrectionAPI.as_view(), name='soumettre-correction'),
    path('solutions/<int:solution_id>/corriger/',CorrigerSolutionAPI.as_view(), name='corriger-solution'),
    path('exercices/<int:exercice_id>/corriger-toutes/', CorrigerToutesSolutionsAPI.as_view(), name='corriger-toutes-solutions'),
]