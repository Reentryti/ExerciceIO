from rest_framework import serializers
from .models import Utilisateur, Classe

class UserSerializer(serializers.ModelSerializer):
    classe = serializers.PrimaryKeyRelatedField(queryset=Classe.objects.all())
    role = serializers.CharField(max_length=20) 

    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'classe', 'role']
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
        return user

class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = ['id', 'nom']  # Champs à sérialiser