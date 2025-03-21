from rest_framework import serializers
from .models import Utilisateur, Classe

class UserSerializer(serializers.ModelSerializer):
    classes_affected = serializers.PrimaryKeyRelatedField(queryset=Classe.objects.all(), many=True, required=False)
    role = serializers.CharField(max_length=20) 

    class Meta:
        model = Utilisateur
        fields = ['id', 'email', 'prenom', 'nom', 'password', 'classes_affected', 'role']
        extra_kwargs = {
            'password': {'write_only': True}, 
        }

    def create(self, validated_data):
        # Extraire les classes et le mot de passe des données validées
        classes_data = validated_data.pop('classes_affected', [])
        password = validated_data.pop('password')
        
        # Création de l'utilisateur avec les données validées
        user = Utilisateur.objects.create_user(**validated_data)
        
        # Définir le mot de passe
        user.set_password(password)
        
        # Associer les classes à l'utilisateur
        if classes_data:
            user.classes_affected.set(classes_data)
            
        # Sauvegarder l'utilisateur
        user.save()
        
        return user

class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = ['id', 'nom']  # Champs à sérialiser