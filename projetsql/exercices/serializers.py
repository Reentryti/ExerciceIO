from rest_framework import serializers
from .models import Exercice, Solution
from utilisateurs.models import Classe

class ExerciceSerializer(serializers.ModelSerializer):
    classe_affected = serializers.PrimaryKeyRelatedField(queryset=Classe.objects.all(), many=True) 

    class Meta:
        model = Exercice
        fields = ['id', 'titre', 'description', 'classe_affected', 'fichier', 'createur', 'date_creation', 'date_a_soumettre']
        #Champs statiques
        read_only_fields = ['createur', 'date_creation']

    def create(self, validated_data):
        validated_data['createur'] = self.context['request'].user
        return super().create(validated_data)

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ['id', 'exercice', 'etudiant', 'fichier', 'commentaire', 'date_soumission']
        read_only_fields = ['etudiant', 'date_soumission']

    def create(self, validated_data):
        validated_data['etudiant'] = self.context['request'].user
        validated_data['exercice'] = self.context['exercice']
        return super().create(validated_data)