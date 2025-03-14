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

    def post(self, request, *args, **kwargs):
        serializer = ExerciceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListeExercicesView(APIView):
    def get(self, request, *args, **kwargs):
        etudiant = request.user
        classes_etudiant = etudiant.classe.all()
        exercices = Exercice.objects.filter(classes__in=classes_etudiant).distinct()
        serializer = ExerciceSerializer(exercices, many=True)
        return Response(serializer.data)

class SoumettreSolutionView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, exercice_id, *args, **kwargs):
        try:
            exercice = Exercice.objects.get(id=exercice_id)
        except Exercice.DoesNotExist:
            return Response({"error": "Exercice non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        if timezone.nom() > exercice.date_a_soumettre:
            return Response({"error":"La date de soumission est dépassée"}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = SolutionSerializer(data=request.data, context={'request': request, 'exercice': exercice})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListeSolutionsView(APIView):
    def get(self, request, exercice_id, *args, **kwargs):
        try:
            exercice = Exercice.objects.get(id=exercice_id)
        except Exercice.DoesNotExist:
            return Response({"error": "Exercice non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        solutions = Solution.objects.filter(exercice=exercice)
        serializer = SolutionSerializer(solutions, many=True)
        return Response(serializer.data)


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