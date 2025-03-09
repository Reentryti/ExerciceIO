from django.shortcuts import render
from django.contrib.auth import login, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, ClasseSerializer   
from .models import Utilisateur, Classe
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime


#Page d'accueil
def index(request):
    return render(request, 'index.html')

#Classe d'inscription
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            #Existence de la classe?
            classe_name = request.data.get('classe')
            if not Classe.objects.filter(nom=classe_name).exists():
                return Response({'error': 'Classe invalide'}, status=status.HTTP_400_BAD_REQUEST)
            #Creation utilisateur
            user = serializer.save()
            user.classe = classe
            user.save()
            login(request, user)
            return Response({"message": "Utilisateur créé avec succès"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Classe classe
class ClasseListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        classes = Classe.objects.all()
        serializer = ClasseSerializer(classes, many=True)
        return Response(serializer.data)

#Classe de connexion
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            #return Response({
             #   "message": "Connexion réussie",
              #  "access": str(refresh.access_token),
               # "refresh": str(refresh),
                #"role": user.role,
            #}, status=status.HTTP_200_OK)
            token, created = Token.objects.get_or_create(user=user)
            role = user.role
            login(request, user)
            return Response({"message": "Connexion réussie", "token": token.key, "role": role,}, status=status.HTTP_200_OK)
        return Response({"error": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)

#Classe de déconnexion
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        request.session.flush()  
        return Response({"message": "Déconnexion réussie"}, status=status.HTTP_200_OK)

#Classe utilisateur
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Récupérer l'utilisateur connecté
        user_data = UserSerializer(user).data
        current_date = datetime.now().strftime("%A %d %B %Y")
        return Response({
            "user":user_data,
            "date":current_date,
        }, status=status.HTTP_200_OK)
        #return Response(serializer.data, status=status.HTTP_200_OK)
    
    #def get_current_date(request):
     #   current_date: datetime.now().strftime("%A %d %B %Y")
      #  return JsonResponse({"date":current_date}) 

#Classe changement de mot de passe
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        # Vérifier l'ancien mot de passe
        if not user.check_password(old_password):
            return Response({"error": "Ancien mot de passe incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        # Changer le mot de passe
        user.set_password(new_password)
        user.save()

        # Mettre à jour la session pour éviter la déconnexion
        update_session_auth_hash(request, user)

        return Response({"message": "Mot de passe changé avec succès"}, status=status.HTTP_200_OK)