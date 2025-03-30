from django.db import models
from django.conf import settings
from exercices.models import Solution
from storages.backends.s3boto3 import S3Boto3Storage


class CorrectionFileStorage(S3Boto3Storage):
    """Stockage S3 personnalisé pour les corrections annotées"""
    location = 'annotated-corrections'
    file_overwrite = False
    default_acl = 'private'
    custom_domain = False

    def get_available_name(self, name, max_length=None):
        """Génère un nom unique pour éviter les conflits"""
        return super().get_available_name(name, max_length)


class Correction(models.Model):
    PROVIDER_CHOICES = [
        ('DEEPSEEK', 'DeepSeek'),
        ('MANUAL', 'Manuelle'),
    ]
    
    solution = models.OneToOneField(Solution, on_delete=models.CASCADE, related_name='correction_rel')
    commentaires = models.TextField(null=True)
    note = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    date_correction = models.DateTimeField(auto_now_add=True)
    corrige_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='DEEPSEEK')
    metadata = models.JSONField(default=dict, blank=True)
    annotated_file = models.FileField(
        storage=CorrectionFileStorage(),
        upload_to='%Y/%m/%d',
        blank=True,
        null=True,
        verbose_name='Document annoté (S3)'
    )

    class Meta:
        verbose_name = "Correction"
        verbose_name_plural = "Corrections"

    def __str__(self):
        return f"Correction de {self.solution}"