from django.urls import path
from .views import SoumettreSolutionAPI,ListeCorrectionAPI, CorrectionDetailAPI

urlpatterns = [
    path('exercices/<int:exercice_id>/soumettre/', SoumettreSolutionAPI.as_view(), name='soumettre-solution'),
    path('corrections/', ListeCorrectionAPI.as_view(), name='liste-corrections'),
    path('corrections/<int:correction_id>/', CorrectionDetailAPI.as_view(), name='correction-detail'),
]