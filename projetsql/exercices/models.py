from django.db import models
from django.conf import settings
from utilisateurs.models import Classe

# Create your models here.

#Modele des exercices
class Exercice(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    createur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exercices_crees')
    classe_affected = models.ManyToManyField(Classe, related_name='exercices', blank=True)
    fichier = models.FileField(upload_to='exercices/', blank=True, null=True)

#Modele des solutions
class Solution(models.Model):
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE, related_name='solutions')
    etudiant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solutions_soumises')
    fichier = models.FileField(upload_to='solutions/')
    date_soumission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solution de {self.etudiant} pour {self.exercice}"
