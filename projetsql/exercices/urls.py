# exercices/urls.py
from django.urls import path
from .views import UploadExerciceView, ListeExercicesView, SoumettreSolutionView, ListeSolutionsView, ProfesseurExercicesView, RecentExerciceView, DetailExerciceView

urlpatterns = [
    path('upload/', UploadExerciceView.as_view(), name='upload_exercice'),
    path('liste/', ListeExercicesView.as_view(), name='liste_exercices'),
    path('<int:exercice_id>/soumettre/', SoumettreSolutionView.as_view(), name='soumettre_solution'),
    path('<int:exercice_id>/solutions/', ListeSolutionsView.as_view(), name='liste_solutions'),
    path('api/professeur/exercices/', ProfesseurExercicesView.as_view(), name='professeur_exercices'),
    path('recent/', RecentExerciceView.as_view(), name='exercice_recent'),
    path('<int:exercice_id>/', DetailExerciceView.as_view(), name='detail_exercice'),  
    path(''),
]