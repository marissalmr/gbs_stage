from django.shortcuts import render
from django import forms

def clean_siret(self):
    siret = self.cleaned_data['siret']
    if len(siret)!=14 or siret.isdigit() :
        raise forms.ValidationError("Le SIRET doit contenir 14 chiffres.")
    
