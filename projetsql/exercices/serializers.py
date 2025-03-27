from rest_framework import serializers
from .models import Exercice, Solution, Note
from utilisateurs.models import Classe

class ExerciceSerializer(serializers.ModelSerializer):
    classes_affected = serializers.PrimaryKeyRelatedField(queryset=Classe.objects.all(), many=True, required=True)
    fichier = serializers.FileField(required=True)

    class Meta:
        model = Exercice
        fields = ['id', 'titre', 'description', 'classes_affected', 'fichier', 'createur', 'date_creation', 'date_a_soumettre']
        read_only_fields = ['createur', 'date_creation']

    def create(self, validated_data):
        #Extraction du fichier
        fichier = validated_data.pop('fichier')

        #Extraction des classes associées
        classes_affected = validated_data.pop('classes_affected', [])

        #Creation de l'exercice pre save
        exercice=Exercice(**validated_data)
        exercice.createur = self.context['request'].user

        #Save for S3
        exercice.fichier.save(fichier.name, fichier, save=True)

        #Association des classes à l'exercice
        exercice.classes_affected.set(classes_affected)

        return exercice

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ['id', 'exercice', 'etudiant', 'fichier', 'date_soumission', 'note']
        read_only_fields = ['etudiant', 'date_soumission', 'exercice']

    def create(self, validated_data):
        validated_data['etudiant'] = self.context['request'].user
        validated_data['exercice'] = self.context['exercice']
        return super().create(validated_data)


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model= Note
        fields =['id', 'valeur', 'solution']