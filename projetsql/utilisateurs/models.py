from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

#Modele de la classe
class Classe(models.Model):
    nom = models.CharField(max_length=25, unique=True)
  
    def __str__(self):
        return self.nom

#Modele de gestion des utilisateurs
class UtilisateurManager(BaseUserManager):
    # Fonction de création d'un utilisateur
    def create_user(self, email, prenom, nom, password=None, **extra_fields):
        """Crée et retourne un utilisateur avec un email, prénom, nom et mot de passe"""
        if not email:
            raise ValueError('L\'email doit être défini')
        email = self.normalize_email(email)
        user = self.model(email=email, prenom=prenom, nom=nom, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Fonction de création d'un superutilisateur
    def create_superuser(self, email, prenom, nom, password=None, **extra_fields):
        """Crée et retourne un super utilisateur"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'professeur')
        return self.create_user(email, prenom, nom, password, **extra_fields)

#Modele personnalisé d'utilisateur
class Utilisateur(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('professeur', 'Professeur'),
        ('etudiant', 'Etudiant'),
    ]
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='etudiant')
    # Classe relatif aux professeurs (multiple)
    classes_affected = models.ManyToManyField(Classe, related_name='professeurs', blank=True)
    # Classe relatif à l'eleve (unique)
    classe = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True)  
    actif = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Utilisation du modèle personnalisé
    objects = UtilisateurManager()

    #Champs utilisé pour l'identification
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['prenom', 'nom']

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.role})"