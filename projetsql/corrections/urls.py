from django.urls import path
from .views import SoumettreSolutionAPI

urlpatterns = [
    path('exercices/<int:exercice_id>/soumettre/', SoumettreSolutionAPI.as_view(), name='soumettre-solution'),
]