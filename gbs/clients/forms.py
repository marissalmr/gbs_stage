from django import forms 
from .models import *

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'email', 'telephone', 'adresse', 'ville', 'code_postal']

class PrediagForm(forms.ModelForm):
    class Meta:
        model = Prediagnostique
        fields = ['question', 'reponse', 'sous_traitee']
        widgets = {
                'sous_traitee': forms.RadioSelect(
                    choices=[
                        (True, "Oui"),
                        (False, "Non"),
                    ]
                )
            }

