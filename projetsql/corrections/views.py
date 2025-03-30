from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Solution, Correction
from .services import CorrectionEngine
from exercices.models import Exercice

# Create your views here.


class SoumettreSolutionAPI(APIView):
    def post(self, request, exercice_id):
        exercice = get_object_or_404(Exercice, pk=exercice_id)
        solution_texte = request.data.get('solution_texte', '')
        
        soumission = Soumission.objects.create(
            exercice=exercice,
            eleve=request.user,
            solution_texte=solution_texte
        )
        
        # Correction automatique avec DeepSeek
        try:
            correction_data = CorrectionEngine(
                exercice.consigne,
                solution_texte
            )
            
            Correction.objects.create(
                soumission=soumission,
                commentaires=correction_data.get('commentaires', ''),
                note=correction_data.get('note'),
                corrige_par=None,
                est_auto_corrigee=True
            )
            
            return Response({
                'status': 'success',
                'correction': correction_data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)