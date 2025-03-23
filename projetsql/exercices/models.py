from django.db import models
from django.conf import settings
from utilisateurs.models import Classe
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

#Modele des exercices
class Exercice(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_a_soumettre = models.DateTimeField()
    createur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exercices_crees')
    classes_affected = models.ManyToManyField(Classe, related_name='exercices', blank=True)
    fichier = models.FileField(upload_to='exercices/')

    def __str__(self):
        return self.titre

    def clean(self):
        if self.date_a_soumettre <= self.date_creation:
            raise ValidationError("La date de soumission doit etre posterieure à la date de creation")

#Modele des solutions
class Solution(models.Model):
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE, related_name='solutions')
    etudiant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solutions_soumises')
    fichier = models.FileField(upload_to='solutions/')
    date_soumission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solution de {self.etudiant} pour {self.exercice}"
