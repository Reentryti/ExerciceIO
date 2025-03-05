from django.urls import path
from .views import index, RegisterView, LoginView, LogoutView, ClasseListView

urlpatterns = [
    # Page d'accueil
    path('', index, name='index'),

    # Inscription (class-based view)
    path('register/', RegisterView.as_view(), name='register'),

    # Connexion (class-based view)
    path('login/', LoginView.as_view(), name='login'),

    # Déconnexion (class-based view)
    path('logout/', LogoutView.as_view(), name='logout'),

    # API pour récupérer les classes
    path('classes/', ClasseListView.as_view(), name='classe-list'),
]