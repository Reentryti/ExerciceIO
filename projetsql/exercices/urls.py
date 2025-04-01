# exercices/urls.py
from django.urls import path
from .views import UploadExerciceView, ListeExercicesView, ExercicesParClasseForProfView, SoumettreSolutionView, ListeSolutionsView, ProfesseurExercicesView, RecentExerciceView, DetailExerciceView, AttribNoteView

urlpatterns = [
    path('upload/', UploadExerciceView.as_view(), name='upload_exercice'),
    path('liste/', ListeExercicesView.as_view(), name='liste_exercices'),
    path('<int:exercice_id>/soumettre/', SoumettreSolutionView.as_view(), name='soumettre_solution'),
    path('<int:exercice_id>/solutions/', ListeSolutionsView.as_view(), name='liste_solutions'),
    path('professeur/exercices/', ProfesseurExercicesView.as_view(), name='professeur_exercices'),
    path('recent/', RecentExerciceView.as_view(), name='exercice_recent'),
    path('<int:exercice_id>/', DetailExerciceView.as_view(), name='detail_exercice'),  
    path('solutions/<int:solution_id>/attribuer-note/', AttribNoteView.as_view(), name='note_attrib'),
    path('professeur/classes/<int:classe_id>/exercices/', ExercicesParClasseForProfView.as_view()),
]