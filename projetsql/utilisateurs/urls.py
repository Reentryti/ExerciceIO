from django.urls import path
from .views import index, RegisterView, LoginView, LogoutView, ClasseListView, UserProfileView, ProfesseurClassesView, GoogleLoginRedirect, google_callback

urlpatterns = [
    # Page d'accueil
    path('', index, name='index'),
    # Inscription
    path('register/', RegisterView.as_view(), name='register'),
    # Connexion
    path('login/', LoginView.as_view(), name='login'),
    # Déconnexion 
    path('logout/', LogoutView.as_view(), name='logout'),
    # API endpoint pour récupérer les classes
    path('classes/', ClasseListView.as_view(), name='classe-list'),
    #API endpoint pour récupérer le nom de l'utilisateur
    path('user/', UserProfileView.as_view(), name='user-profile'),
    path('professeur/classes/', ProfesseurClassesView.as_view(), name='professeur_classes'),
    #API endpoint pour connexion via google
    path('auth/google/login/', GoogleLoginRedirect.as_view(), name='google_login'),
    path('auth/google/callback/', google_callback, name='google_callback'),
]