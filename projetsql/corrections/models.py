from django.db import models
from exercices.models import Solution
#from utilisateurs.models import Utilisateur

# Create your models here.

class Correction(models.Model):
    IA_PROVIDERS = [('DEEPSEEK', 'DeepSeek'),('OLLAMA', 'Ollama'),]

    solution = models.OneToOneField(Solution, on_delete=models.CASCADE, related_name='correction')
    created_at = models.DateTimeField(auto_now_add=True)
    provider = models.CharField(max_length=20, choices=IA_PROVIDERS)
    raw_response = models.JSONField()  # Réponse brute de l'IA
    feedback = models.TextField()      # Feedback formaté
    score = models.FloatField(null=True, blank=True)
    #corrected_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='corrections')
    


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Correction #{self.id} pour {self.solution}"