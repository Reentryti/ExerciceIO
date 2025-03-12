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
            'date_a_soumettre': forms.DateTimeInput(attrs={'type':'datetime-local'}),
            'description' : forms.Textarea(attrs={'rows':4}),
            'classes' : forms.CheckboxSelectMultiple,
        }
        
    def clean_date_a_soumettre(self):
        date_a_soumettre = self.cleaned_data.get('date_a_soumettre')
        if date_a_soumettre and date_a_soumettre < timezone.now():
            raise ValidationError("La date de soumission passée.")
        return date_a_soumettre

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

