from django.shortcuts import render
from django.contrib.auth import login, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, ClasseSerializer   
from .models import Utilisateur, Classe

# Page d'accueil
def index(request):
    return render(request, 'index.html')

# Classe d'inscription
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Vérifier si la classe existe
            classe_name = request.data.get('classe')
            if not Classe.objects.filter(nom=classe_name).exists():
                return Response({'error': 'Classe invalide'}, status=status.HTTP_400_BAD_REQUEST)

            # Créer l'utilisateur
            user = serializer.save()
            login(request, user)
            return Response({"message": "Utilisateur créé avec succès"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClasseListView(APIView):
    permission_classes = [AllowAny]  # Autoriser tout le monde à accéder à cette vue

    def get(self, request):
        classes = Classe.objects.all()  # Récupérer toutes les classes
        serializer = ClasseSerializer(classes, many=True)  # Sérialiser les données
        return Response(serializer.data)  # Renvoyer la réponse

# Classe de connexion
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return Response({"message": "Connexion réussie"}, status=status.HTTP_200_OK)
        return Response({"error": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)

# Classe de déconnexion
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.session.flush()  # Nettoyer la session
        return Response({"message": "Déconnexion réussie"}, status=status.HTTP_200_OK)