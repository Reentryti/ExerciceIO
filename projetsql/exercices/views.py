from django.shortcuts import render
from .models import Exercice, Solution
from django import forms
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExerciceSerializer, SolutionSerializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class UploadExerciceView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"error":"Acces refusé"}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = ExerciceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Liste Exercice
class ListeExercicesView(APIView):
    def get(self, request, *args, **kwargs):
        etudiant = request.user
        if not etudiant or not hasattr(etudiant, 'classe') or not etudiant.classe:
            return Response({"error":"Etudiant sans classe"}, status=status.HTTP_400_BAD_REQUEST)

        #classe_etudiant = [etudiant.classe] if etudiant.classe else []
        classe_etudiant = etudiant.classe
        exercices = Exercice.objects.filter(classes_affected=classe_etudiant).distinct()
        serializer = ExerciceSerializer(exercices, many=True)
        return Response(serializer.data)

#Soumission Exercice
class SoumettreSolutionView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, exercice_id, *args, **kwargs):
        try:
            exercice = Exercice.objects.get(id=exercice_id)
        except Exercice.DoesNotExist:
            return Response({"error": "Exercice non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        if timezone.now() > exercice.date_a_soumettre:
            return Response({"error":"La date de soumission est dépassée"}, status=status.HTTP_400_BAD_REQUEST)
            
        #Sauvegarde de la solution
        serializer = SolutionSerializer(data=request.data, context={'request': request, 'exercice': exercice})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Liste Soumission Exercice
class ListeSolutionsView(APIView):
    def get(self, request, exercice_id, *args, **kwargs):
        try:
            exercice = Exercice.objects.get(id=exercice_id)
        except Exercice.DoesNotExist:
            return Response({"error": "Exercice non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        solutions = Solution.objects.filter(exercice=exercice)
        serializer = SolutionSerializer(solutions, many=True)
        return Response(serializer.data)

#Recent Exercice
class RecentExerciceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        etudiant = request.user
        
        # Ajoutez des logs pour le débogage
        print(f"Utilisateur: {etudiant.email}, ID: {etudiant.id}")
        print(f"Classe de l'utilisateur: {etudiant.classe if hasattr(etudiant, 'classe') else 'Aucune'}")

        if not etudiant or not hasattr(etudiant, 'classe') or not etudiant.classe:
            return Response({"error":"Utilisateur non connecté ou sans classe"}, status=status.HTTP_400_BAD_REQUEST)

        classe_id = etudiant.classe.id
        
        try:
            # Recherche des exercices pour la classe de l'étudiant
            exercices = Exercice.objects.filter(classes_affected__id=classe_id).distinct()
            print(f"Nombre d'exercices trouvés: {exercices.count()}")
            
            # Obtenir l'exercice le plus récent (notez le - devant date_creation)
            exercice_recent = exercices.order_by('-date_creation').first()

            if exercice_recent:
                print(f"Exercice récent trouvé: {exercice_recent.id} - {exercice_recent.titre}")
                serializer = ExerciceSerializer(exercice_recent)
                return Response(serializer.data)
            else:
                print("Aucun exercice récent trouvé")
                return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(f"Erreur: {str(e)}")
            return Response({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProfesseurExercicesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Vérifier que l'utilisateur est un professeur
        if not request.user.is_staff:
            return Response({"error": "Accès refusé. Seuls les professeurs peuvent accéder à cette ressource."}, status=status.HTTP_403_FORBIDDEN)

        # Récupérer les exercices créés par le professeur connecté
        exercices = Exercice.objects.filter(createur=request.user)
        serializer = ExerciceSerializer(exercices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)