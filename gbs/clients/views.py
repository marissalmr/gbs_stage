from django.shortcuts import redirect, render
from .forms import *

def clean_siret(self):
    siret = self.cleaned_data['siret']
    if len(siret)!=14 or siret.isdigit() :
        raise forms.ValidationError("Le SIRET doit contenir 14 chiffres.")
    
def prediag_view(request):
    form = None 
    if request.method == "POST" : 
        form = PrediagForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect("thanks")
        else:
            form = PrediagForm()
    return render(request, "clients/prediag_form.html", {"form": form})
