from django.contrib import admin
from .models import Classe,Utilisateur

# Register your models here.
#Ajout de la classe dans register
admin.site.register(Classe)

class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'role', 'is_staff')  # Champs à afficher dans la liste
    search_fields = ('nom', 'email')  # Champs de recherche
    list_filter = ('role', 'is_staff')  # Filtres

# Enregistrez le modèle avec la classe Admin personnalisée
admin.site.register(Utilisateur, UtilisateurAdmin)