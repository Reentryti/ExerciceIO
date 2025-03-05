from rest_framework import serializers
from .models import Utilisateur, Classe

class UserSerializer(serializers.ModelSerializer):
    classe = serializers.PrimaryKeyRelatedField(queryset=Classe.objects.all())  # Valider l'existence de la classe
    role = serializers.CharField(max_length=20)  # Ajouter le champ role

    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'classe', 'role']
        extra_kwargs = {
            'password': {'write_only': True},  # Masquer le mot de passe dans les réponses
        }

    def create(self, validated_data):
        # Extraire le mot de passe pour le hasher
        password = validated_data.pop('password')
        # Créer l'utilisateur avec les données validées
        user = Utilisateur.objects.create_user(**validated_data)
        # Définir le mot de passe
        user.set_password(password)
        user.save()
        return user

class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = ['id', 'nom']  # Champs à sérialiser