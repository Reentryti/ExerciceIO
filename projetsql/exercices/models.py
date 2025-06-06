from django.db import models
from django.conf import settings
from utilisateurs.models import Classe
from django.utils import timezone
from django.core.exceptions import ValidationError
from storages.backends.s3boto3 import S3Boto3Storage
# Create your models here.

#Modele des exercices
class Exercice(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_a_soumettre = models.DateTimeField()
    createur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exercices_crees')
    classes_affected = models.ManyToManyField(Classe, related_name='exercices', blank=True)
    fichier = models.FileField(upload_to='exercices/', storage=S3Boto3Storage(), verbose_name='Fichier S3')

    def __str__(self):
        return self.titre

    def clean(self):
        if self.date_a_soumettre <= self.date_creation:
            raise ValidationError("La date de soumission doit etre posterieure à la date de creation")

#Modele des solutions
class Solution(models.Model):
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE, related_name='solutions')
    etudiant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solutions_soumises')
    fichier = models.FileField(upload_to='solutions/', storage=S3Boto3Storage(), verbose_name='Fichier S3')
    date_soumission = models.DateTimeField(auto_now_add=True)
    note = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0.00)

    @property
    def correction(self):
        """Version optimisée avec cache"""
        if not hasattr(self, '_correction_cache'):
            self._correction_cache = getattr(self, 'correction_rel', None)
        return self._correction_cache

    def trigger_correction(self, provider="DEEPSEEK"):
        """Méthode robuste pour lancer une correction"""
        from corrections.services import CorrectionEngine
        try:
            return CorrectionEngine.create_correction(self, provider)
        except Exception as e:
            raise CorrectionError(f"Échec de la correction: {str(e)}")


    def __str__(self):
        return f"Solution de {self.etudiant} pour {self.exercice}"


#Modele note
class Note(models.Model):
    solution = models.OneToOneField(Solution, on_delete=models.CASCADE, related_name='note_attrib')
    valeur = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"Note {self.valeur} pour {self.solution}"