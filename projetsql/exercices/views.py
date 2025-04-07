from django.shortcuts import render
from .models import Exercice, Solution, Note
from django import forms
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExerciceSerializer, SolutionSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from .plagiat import analyse_nlp

# Create your views here.

#View pour créer et uploader des exercices
class UploadExerciceView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Vérification des permissions
        if not request.user.is_staff:
            return Response(
                {"error": "Accès réservé aux professeurs"}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # Vérification manuelle du fichier
        if 'fichier' not in request.FILES:
            return Response(
                {"error": "Aucun fichier fourni"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:

            data = request.data.copy()
            if 'classes_affected' in data:
                if isinstance(data['classes_affected'], str):
                    data.setlist('classes_affected', [data['classes_affected']])

            serializer = ExerciceSerializer(
                data=data,
                context={
                    'request': request,
                    'file': request.FILES['fichier']
                }
            )

            if serializer.is_valid(raise_exception=True):
                exercice = serializer.save()
                
                #Vérification que le fichier est bien sur S3
                if not exercice.fichier.url.startswith('https://'):
                    raise ValidationError("Le fichier n'a pas été uploadé vers S3")

                return Response(
                    {
                        "message": "Exercice créé avec succès",
                        "data": serializer.data,
                        "s3_url": exercice.fichier.url
                    },
                    status=status.HTTP_201_CREATED
                )

        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            return Response(
                {"error": f"Erreur serveur: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


#View pour lister les exercices disponibles pour l'étudiant
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


#View pour lister les exercices d'une classe pour le professeur
class ExercicesParClasseForProfView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, classe_id):
        # Vérifie que l'utilisateur est un professeur
        if not request.user.is_staff:
            return Response({"error": "Accès réservé aux professeurs"}, status=403)

        exercices = Exercice.objects.filter(
            createur=request.user,
            classes_affected__id=classe_id
        ).distinct()

        serializer = ExerciceSerializer(exercices, many=True)
        return Response(serializer.data)


#View pour soumettre une solution d'exercice
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


#View pour lister les solutions d'un exercice
class ListeSolutionsView(APIView):
    def get(self, request, exercice_id, *args, **kwargs):
        try:
            exercice = Exercice.objects.get(id=exercice_id)
        except Exercice.DoesNotExist:
            return Response({"error": "Exercice non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        solutions = Solution.objects.filter(exercice=exercice)
        serializer = SolutionSerializer(solutions, many=True)
        return Response(serializer.data)


#View pour retourner l'exercice le plus récent
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


#View pour lister les exercices crées d'un professeur
class ProfesseurExercicesView(APIView):
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Vérifier que l'utilisateur est un professeur
        if not request.user.is_staff:
            return Response({"error": "Accès refusé."}, status=status.HTTP_403_FORBIDDEN)

        # Récupérer les exercices créés par le professeur connecté
        exercices = Exercice.objects.filter(createur=request.user)
        page = self.pagination_class().paginate_queryset(exercices, request)
        serializer = ExerciceSerializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#View pour afficher les détails d'un exercice
class DetailExerciceView(APIView):
    def get(self, request, exercice_id):
        try:
            exercice = Exercice.objects.get(id=exercice_id)
            serializer = ExerciceSerializer(exercice)
            return Response(serializer.data)
        except Exercice.DoesNotExist:
            return Response({"error": "Exercice non trouvé."}, status=status.HTTP_404_NOT_FOUND)


#Vue d'attribution de note
class AttribNoteView(APIView):
    def post(self, request, solution_id):
        try:
            solution = Solution.objects.get(id=solution_id)
            #Validation de la note
            note = request.data.get('valeur')
            if not note or float(note) < 0 or float(note) > 20:
                return Response({"error": "La note doit etre comprise entre 0 et 20 strictement"}, status =status.HTTP_400_BAD_REQUEST)
            solution.note = note
            solution.save()
            return Response({"message": "Note attribuée avec succés", "note": solution.note}, status = status.HTTP_200_OK)
        except Solution.DoesNotExist:
            return Response({"error": "Solution non existante"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)


        #serialiser = NoteSerializer(data=request.data)
        #if serialiser.is_valid():
         #   serialiser.save(solution=solution)
          #  return Response(serialiser.data, status=status.HTTP_201_CREATED)
        #return Response(serialiser.data, status=status.HTTP_400_BAD_REQUEST)


#Vue detection de plagiat
class PlagiatDetection(APIView):
    def get(self, request, exercice_id):
        solutions = Solution.objects.filter(exercice_id=exercice_id)
        if len(solutions) < 2:
            return Response({"message": "Pas assez de solutions pour detecter d'eventuel plagiat"}, status=200)
        
        resultat = analyse_nlp(solutions)
        
        return Response(resultat)
