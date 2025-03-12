from rest_framework import serializers
from .models import Utilisateur, Classe

class UserSerializer(serializers.ModelSerializer):
    classes = serializers.PrimaryKeyRelatedField(queryset=Classe.objects.all(), many=True)
    role = serializers.CharField(max_length=20) 

    class Meta:
        model = Utilisateur
        fields = ['id', 'email', 'prenom', 'nom', 'password', 'classe', 'classes', 'role']
        extra_kwargs = {
            'password': {'write_only': True}, 
        }

    def create(self, validated_data):
        #Hash du mot de passe
        password = validated_data.pop('password')
        #Creation de l'utilisateur avec les donnees valides
        user = Utilisateur.objects.create_user(**validated_data)
        #Mot de passe
        user.set_password(password)
        user.save()
        print("Données reçues après validation :", validated_data)
        return user

class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = ['id', 'nom']  # Champs à sérialiser