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

#Vue pour la correction par IA
class SoumettreCorrectionAPI(APIView):
    def post(self, request, exercice_id):
        #Recuperation de l'exercice
        exercice = get_object_or_404(Exercice, pk=exercice_id)
        #Si solution
        exist_solution = Solution.objects.filter(
            exercice=exercice,
            etudiant=request.user
        ).first()
        
        if exist_solution:
            return Response({'status':'error','message':'Solution deja existante'}, status=status.HTTP_400_BAD_REQUEST)

        #Solution
        solution = Solution.objects.create(
            exercice=exercice,
            etudiant =request.user,
            fichier=request.FILES.get('fichier'),
            note=0.00 #Note par défaut
        )

        # Correction automatique avec DeepSeek
        try:
            correction = solution.trigger_correction(provider="DEEPSEEK")
            
            return Response({'status': 'success', 'solution': solution.id, 'correction': {
                'note': float(solution.note),
                'commentaires':correction.commentaires if hasattr (correction, 'commentaire') else ''
            }}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            solution.delete()
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CorrigerSolutionAPI(APIView):
    def post(self, request, solution_id):
        try:
            solution = Solution.objects.get(pk=solution_id)
            correction = solution.trigger_correction(provider="DEEPSEEK")
            
            return Response({
                'status': 'success',
                'note': solution.note,
                'commentaires': getattr(correction, 'commentaires', '')
            }, status=status.HTTP_200_OK)
            
        except Solution.DoesNotExist:
            return Response({'status': 'error', 'message': 'Solution non trouvée'}, status=404)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CorrigerToutesSolutionsAPI(APIView):
    def post(self, request, exercice_id):
        try:
            exercice = Exercice.objects.get(pk=exercice_id)
            solutions = exercice.solutions.all()
            
            results = []
            engine = CorrectionEngine()
            
            for solution in solutions:
                correction = engine.create_correction(solution, "DEEPSEEK")
                results.append({
                    'solution_id': solution.id,
                    'note': solution.note,
                    'status': 'success'
                })
            
            return Response({
                'status': 'success',
                'results': results
            }, status=status.HTTP_200_OK)
            
        except Exercice.DoesNotExist:
            return Response({'status': 'error', 'message': 'Exercice non trouvé'}, status=404)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)