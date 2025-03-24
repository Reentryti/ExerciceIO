from rest_framework import serializers
from .models import Exercice, Solution, Note
from utilisateurs.models import Classe

class ExerciceSerializer(serializers.ModelSerializer):
    classes_affected = serializers.PrimaryKeyRelatedField(queryset=Classe.objects.all(), many=True, required=True)

    class Meta:
        model = Exercice
        fields = ['id', 'titre', 'description', 'classes_affected', 'fichier', 'createur', 'date_creation', 'date_a_soumettre']
        read_only_fields = ['createur', 'date_creation']

    def create(self, validated_data):
        #Extraction des classes associées
        classes_affected = validated_data.pop('classes_affected', [])

        #Association utilisateur connecté comme créateur de l'exercice
        validated_data['createur'] = self.context['request'].user

        #Création de l'exercice
        exercice = Exercice.objects.create(**validated_data)

        #Association des classes à l'exercice
        exercice.classes_affected.set(classes_affected)

        return exercice

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ['id', 'exercice', 'etudiant', 'fichier', 'commentaire', 'date_soumission', 'note']
        read_only_fields = ['etudiant', 'date_soumission', 'exercice']

    def create(self, validated_data):
        validated_data['etudiant'] = self.context['request'].user
        validated_data['exercice'] = self.context['exercice']
        return super().create(validated_data)


class NoteSerializer(serializer.ModelSerializer):
    class Meta:
        model= Note
        fields =['id', 'valeur', 'solution']