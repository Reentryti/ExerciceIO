from rest_framework import serializers
from .models import Utilisateur, Classe

class UserSerializer(serializers.ModelSerializer):
    classes_affected = serializers.PrimaryKeyRelatedField(queryset=Classe.objects.all(), many=True)
    role = serializers.CharField(max_length=20) 

    class Meta:
        model = Utilisateur
        fields = ['id', 'email', 'prenom', 'nom', 'password', 'classe', 'classes_affected', 'role']
        extra_kwargs = {
            'password': {'write_only': True}, 
        }

    def create(self, validated_data):
        classes_data = validated_data.pop('classe',[])
        print("Classes reçues :", classes_data)  # Debug
        #Hash du mot de passe
        password = validated_data.pop('password')
        #Creation de l'utilisateur avec les donnees valides
        user = Utilisateur.objects.create_user(**validated_data)
        #Mot de passe
        user.set_password(password)

        if classes_data:
            user.classes.set(classes_data)
        user.classes.set(classes_data)
        user.save()
        print("Données reçues après validation :", validated_data)
        print("classes associés", user.classes.all())
        return user

class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = ['id', 'nom']  # Champs à sérialiser