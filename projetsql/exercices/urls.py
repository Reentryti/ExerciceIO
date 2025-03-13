# exercices/urls.py
from django.urls import path
from .views import UploadExerciceView, ListeExercicesView, SoumettreSolutionView, ListeSolutionsView, ProfesseurExercicesView

urlpatterns = [
    path('upload/', UploadExerciceView.as_view(), name='upload_exercice'),
    path('liste/', ListeExercicesView.as_view(), name='liste_exercices'),
    path('<int:exercice_id>/soumettre/', SoumettreSolutionView.as_view(), name='soumettre_solution'),
    path('<int:exercice_id>/solutions/', ListeSolutionsView.as_view(), name='liste_solutions'),
    path('api/professeur/exercices/', ProfesseurExercicesView.as_view(), name='professeur_exercices'),
]