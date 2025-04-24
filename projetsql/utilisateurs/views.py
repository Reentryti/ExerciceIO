from django.shortcuts import render
from django.contrib.auth import login, authenticate
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, ClasseSerializer   
from .models import Utilisateur, Classe
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
import logging
import requests
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialApp, SocialAccount
from django.core.exceptions import ObjectDoesNotExist
from urllib.parse import urlencode

logger = logging.getLogger(__name__)
#Page d'accueil
def index(request):
    return render(request, 'index.html')

#Classe d'inscription
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Récupération des classes à partir des IDs fournis
            classes_ids = request.data.get("classes_affected", [])
            classes = Classe.objects.filter(id__in=classes_ids)

            if not classes.exists():
                return Response({"error": "Aucune classe valide trouvée"}, status=status.HTTP_400_BAD_REQUEST)

            # Création de l'utilisateur
            user = serializer.save()
            user.classes_affected.set(classes)  # Associer les classes au professeur
            user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
        user = request.user
        user_data = UserSerializer(user).data
        current_date = datetime.now().strftime("%A %d %B %Y")

        #Ajout de classe pour les users n'en ayant pas
        if not user.classe:
            classes = Classe.objects.all()
            classes_data = [{"id":c.id, "nom":c.nom} for c in classes]
        else:
            classes_data = None

        return Response({
            "user":user_data,
            "date":current_date,
            "classes":classes_data
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

#Vue pour assigner les classes
class AssignClasseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        classe_id = request.data.get('classe_id')

        if not classe_id:
            return Response({"error": "Id CLasse requis"}, status = status.HTTP_400_BAD_REQUEST)
        try:
            classe = Classe.objects.get(id=classe_id)
        except Classe.DoesNotExist:
            return Response({"error": "Classe non existante"}, status = status.HTTP_404_NOT_FOUND)

        #Verifions que l'Utilisateur na pas de classe
        if user.classe:
            return Response({"error": "Vous avez deja une classe"}, status = status.HTTP_400_BAD_REQUEST)

        user.classe = classe
        user.save()
        return Response({"succés":"Classe attribuée avec succés"}, status =status.HTTP_200_OK)
        

class ProfesseurClassesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Vérifier que l'utilisateur est un professeur
        if not request.user.is_staff:
            return Response({"error": "Accès refusé. Seuls les professeurs peuvent accéder à cette ressource."}, status=status.HTTP_403_FORBIDDEN)

        # Récupérer les classes affectées au professeur connecté
        classes_affected = request.user.classes_affected.all()
        serializer = ClasseSerializer(classes_affected, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Oauth2 Authentification
#class GoogleLoginView(APIView):
 #   permission_classes = [AllowAny]

  #  def post(self, request):
   #     token = request.data.get('token')
    #    try :
     #       idinfo = id_token.verify_oauth2_token(
      #          token, 
       #         google_requests.Request(),
        #        settings.GOOGLE_CLIENT_ID   
         #   )

          #  email = idinfo.get('email')
           # prenom = idinfo.get('given_name')
            #nom = idinfo.get('family_name')

            #try:
             #   user = Utilisateur.objects.get(email=email)
            #except Utilisateur.DoesNotExist:
            #    user = Utilisateur.objects.create(
             #       email  = email,
              #      prenom =   prenom,
               #     nom = nom,
                #)

                #default_classes = request.data.get("classes", [])
                #if default_classes:
                 #   classes = Classe.objects.filter(id__in= default_classes)
                  #  if classes.exists():
                   #     user.classes.set(classes)
                #user.save()

            #login(request, user, backend='')
            #token, created = Token.objects.get_or_create(user=user)

            #return Response({
             #   "message" : "Connexion avec Google réussie",
              #  "token": token.key,
               # "role": user.role,
                #"nom": nom,
                #"prenom": prenom
            #}, status=status.HTTP_200_OK)
        
        #except ValueError:
         #   return Response({"error":"Token invalide"}, status=status.HTTP_401_UNAUTHORIZED)


#Vue pour l'authentification Google
class GoogleLoginRedirect(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            #Google adapter
            adapter = GoogleOAuth2Adapter(request=request)
            #App provider de google 
            app = SocialApp.objects.get(provider='google')
            #Url authentification
            authorize_url = adapter.authorize_url
            callback_url = f"{settings.SITE_URL}/api/auth/google/callback/"
            state = adapter.stateFromRequest(request) if hasattr(adapter, 'stateFromRequest') else None
            
            #Parametres
            params = {
                'client_id': app.client_id,
                'redirect_uri': callback_url,
                'scope': 'email profile openid',
                'response_type': 'code',
                'access_type': 'offline',
            }
            if state:
                params['state'] = state   
            #Url redirection
            auth_url = f"{authorize_url}?{urlencode(params)}"
            return redirect(auth_url)
            
        except Exception as e:
            logger.error(f"Google login error: {str(e)}", exc_info=True)
            return Response({"error": "Authentication error"}, status=500)


#Authentification callback
def google_callback(request):
    code = request.GET.get('code')
    error = request.GET.get('error')
    
    if error:
        logger.error(f"Error returned by Google: {error}")
        return redirect(f"{settings.FRONTEND_URL}/login?error=google_{error}")
    
    if not code:
        logger.error("No authorization code received")
        return redirect(f"{settings.FRONTEND_URL}/login?error=no_code")

    try:
        adapter = GoogleOAuth2Adapter(request=request)
        app = SocialApp.objects.get(provider='google')
        #Code a token
        token_url = adapter.access_token_url
        callback_url = f"{settings.SITE_URL}/api/auth/google/callback/"
        #Parametres token
        token_params = {
            'code': code,
            'client_id': app.client_id,
            'client_secret': app.secret,
            'redirect_uri': callback_url,
            'grant_type': 'authorization_code',
        }
        token_response = requests.post(token_url, data=token_params).json()
        access_token = token_response.get('access_token')
        
        if not access_token:
            logger.error(f"Failed to get access token: {token_response}")
            return redirect(f"{settings.FRONTEND_URL}/login?error=token_error")
            
        #Recuperation user informations
        userinfo_url = "https://openidconnect.googleapis.com/v1/userinfo"
        headers = {'Authorization': f'Bearer {access_token}'}
        user_data = requests.get(userinfo_url, headers=headers).json()
    
        if 'error' in user_data:
            logger.error(f"Google API Error: {user_data['error']}")
            return redirect(f"{settings.FRONTEND_URL}/login?error=api_error")
        
        try:
            social_account = SocialAccount.objects.get(provider='google', uid=user_data['sub'])
            user = social_account.user
        except SocialAccount.DoesNotExist:
    
            User = get_user_model()
            #Creation de l'Utilisateur
            user = User.objects.create(
                email=user_data['email'],
                prenom=user_data.get('given_name', ''),
                nom=user_data.get('family_name', ''),
                role='etudiant'
            )
            #Creation du compte social
            SocialAccount.objects.create(
                user=user,
                provider='google',
                uid=user_data['sub'],
                extra_data=user_data
            )

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        token, _ = Token.objects.get_or_create(user=user)
        #Redirection
        dashboard_path = '/auth/callback'
        redirect_url = f"{settings.FRONTEND_URL}{dashboard_path}?token={token.key}&email={user.email}&user_id={user.id}&role={user.role}"
        print(f"REDIRECTION URL: {redirect_url}")
        print(f"settings.FRONTEND_URL: {settings.FRONTEND_URL}")
        print(f"dashboard_path: {dashboard_path}")

        #If token create
        print(f"User: {user.email}, Token: {token.key}, Role: {user.role}")

        return redirect(redirect_url)
                
    except Exception as e:
        logger.error(f"Google authentication error: {str(e)}", exc_info=True)
        return redirect(f"{settings.FRONTEND_URL}/login?error=auth_failed")