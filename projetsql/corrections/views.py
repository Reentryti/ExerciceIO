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

#Liste des corrections
class ListeCorrectionAPI(APIView):
    """API pour lister les corrections d'un élève"""
    
    def get(self, request):
        # Filtrer par élève si l'utilisateur est un élève
        user = request.user
        
        # Si l'utilisateur est un enseignant, on peut renvoyer toutes les corrections
        # Sinon, on filtre pour n'avoir que celles de l'élève
        if user.is_staff or user.groups.filter(name='enseignants').exists():
            corrections = Correction.objects.all().order_by('-date_correction')
        else:
            corrections = Correction.objects.filter(
                solution__eleve=user
            ).order_by('-date_correction')
        
        # Sérialisation des données
        data = []
        for correction in corrections:
            try:
                exercice_titre = correction.solution.exercice.titre
                exercice_id = correction.solution.exercice.id
            except:
                exercice_titre = "Sans titre"
                exercice_id = None
                
            correction_data = {
                'id': correction.id,
                'note': float(correction.note) if correction.note else None,
                'commentaires': correction.commentaires,
                'date_correction': correction.date_correction.isoformat(),
                'provider': correction.provider,
                'solution': {
                    'id': correction.solution.id,
                    'exercice': {
                        'id': exercice_id,
                        'titre': exercice_titre
                    }
                }
            }
            
            if correction.annotated_file:
                correction_data['annotated_file'] = request.build_absolute_uri(correction.annotated_file.url)
                
            data.append(correction_data)
        
        return Response(data)


class CorrectionDetailAPI(APIView):
    """API pour obtenir le détail d'une correction"""
    
    def get(self, request, correction_id):
        correction = get_object_or_404(Correction, id=correction_id)
        
        # Vérifier que l'utilisateur a le droit d'accéder à cette correction
        user = request.user
        if not (user.is_staff or user.groups.filter(name='enseignants').exists()):
            if correction.solution.eleve != user:
                return Response(
                    {"error": "Vous n'avez pas accès à cette correction"},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        try:
            exercice_titre = correction.solution.exercice.titre
            exercice_id = correction.solution.exercice.id
        except:
            exercice_titre = "Sans titre"
            exercice_id = None
            
        data = {
            'id': correction.id,
            'note': float(correction.note) if correction.note else None,
            'commentaires': correction.commentaires,
            'date_correction': correction.date_correction.isoformat(),
            'provider': correction.provider,
            'solution': {
                'id': correction.solution.id,
                'texte': correction.solution.texte,
                'exercice': {
                    'id': exercice_id,
                    'titre': exercice_titre
                }
            }
        }
        
        if correction.annotated_file:
            data['annotated_file'] = request.build_absolute_uri(correction.annotated_file.url)
            
        return Response(data)