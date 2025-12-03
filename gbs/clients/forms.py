from django import forms 
from .models import *

class ClientForm(forms.ModelForm):
    model = Client
    exclude = [['nom', 'email', 'telephone', 'adresse', 'ville', 'code_postal', 'siret']]
