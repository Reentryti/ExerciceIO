from django.urls import path
from .views import index, RegisterView, LoginView, LogoutView, ClasseListView, UserProfileView

urlpatterns = [
    # Page d'accueil
    path('', index, name='index'),
    # Inscription
    path('register/', RegisterView.as_view(), name='register'),
    # Connexion
    path('login/', LoginView.as_view(), name='login'),
    # Déconnexion 
    path('logout/', LogoutView.as_view(), name='logout'),
    # API pour récupérer les classes
    path('classes/', ClasseListView.as_view(), name='classe-list'),
    #API pour récupérer le nom de l'utilisateur
    path('user/', UserProfileView.as_view(), name='user-profile'),
]