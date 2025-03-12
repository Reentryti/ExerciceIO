from django import forms
from .models import Exercice
from utilisateurs.models import Classe


#Formulaire d'exercice
class ExerciceForm(forms.Model):
    fileExercice = forms.FileField(required=False, label="Fichier de l'exercice")#champ upload de l'exercice

    #Suivant le model exercice
    class Meta:
        model = Exercice
        fields = ['titre', 'description', 'classe_affected', 'fileExercice']
        widgets = {
            'date_a_soumettre': forms.DateTimeInput(attrs={''}),
            'description' : forms.Textarea(attrs={'rows':4}),
            'classes' : forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


#Formulaire de la solution
class SolutionForm(forms.Model):
    fileSolution = forms.FileField(label="Fichier de la solution")

    #Suivant le model solution
    class Meta:
        model = Solution
        fields = ['fileSolution']


class MultipleInput(forms.ClearableFileInput):
    allow_multiple_selected = True

