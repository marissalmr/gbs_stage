from django import forms 
from .models import *

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'email', 'telephone', 'adresse', 'ville', 'code_postal', 'siret']

class PrediagForm(forms.ModelForm):
    model = Prediagnostique
    fields = ['question', 'reponse']

