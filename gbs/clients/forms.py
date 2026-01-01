from django import forms 
from .models import *

class ClientForm(forms.ModelForm):
    class Meta:
        model = Contact
    
        fields = ['nom', 'email', 'telephone', 'adresse', 'ville', 'code_postal']

from django import forms

class QuestionnaireForm(forms.Form):
    # Ce formulaire NE correspond PAS à une table de la base de données
    # Il est construit dynamiquement à partir des questions stockées en base

    def __init__(self, *args, **kwargs):
        # On récupère la liste des questions envoyée par la vue
        # Exemple : questions = Question.objects.all()
        questions = kwargs.pop("questions")

        # On appelle le constructeur de base de Django
        # Cela initialise le formulaire (création de self.fields = {})
        super().__init__(*args, **kwargs)

        # On parcourt chaque question récupérée depuis la base
        for question in questions:
            choices_list = question.choices if question.choices else []

            # CAS 1 : question à choix UNIQUE (radio buttons)
            if question.type == "single":
                self.fields[str(question.id)] = forms.ChoiceField(
                    # Texte affiché au-dessus des choix
                    label=question.texte_question,
                    choices=choices_list,

                    # Affichage sous forme de boutons radio
                    widget=forms.RadioSelect,

                    # Champ obligatoire
                    required=True,

                   
                )

            # CAS 2 : question à choix MULTIPLES (cases à cocher)
            elif question.type == "multiple":
                self.fields[str(question.id)] = forms.MultipleChoiceField(
                    # Texte affiché au-dessus des choix
                    label=question.texte_question,
                    choices=choices_list,
                   
                    # Affichage sous forme de cases à cocher
                    widget=forms.CheckboxSelectMultiple,
                     

                    # Champ obligatoire
                    required=True,
                )
