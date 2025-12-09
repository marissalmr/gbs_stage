from urllib import response
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .forms import *
from .api import *

def clean_siret(self):
    siret = self.cleaned_data['siret']
    if len(siret)!=14 or siret.isdigit() :
        raise forms.ValidationError("Le SIRET doit contenir 14 chiffres.")
    
def prediag_view(request):
    form = None 
    if request.method == "POST" : 
        form = PrediagForm(request) 
        if form.is_valid():
            form.save()
            return redirect("thanks")
        else:
            form = PrediagForm()
    return render(request, "clients/prediag_form.html", {"form": form})

def check_siret(request):
     # 1. Récupération du SIRET envoyé dans l'URL 
    siret = request.GET.get("siret")
    # 2. Si aucun SIRET fourni → erreur 400 (mauvaise requête)

    if not siret:
        return JsonResponse(
            {"error": "Aucun SIRET fourni dans la requête."},
            status=400  # 400 = erreur du client
        )
    
    data = response.json()["etablissement"]
    
    entreprise_info = {
        "siret": data["siren"],
        "date_creation": data["categorieJuridiqueUniteLegale"].get("dateCreationUniteLegale"),
        "statut_admin": data["etatAdministratifUniteLegale"],
        "nom_officiel": data["denominationUniteLegale"],
        "autres_noms": data["denominationUsuelle1UniteLegale, denominationUsuelle2UniteLegale, denominationUsuelle3UniteLegale"], 
        "prenom_dirigeant": data["nomUsageUniteLegale"].get("prenom1UniteLegale à prenom4UniteLegale"),
}
    return JsonResponse({"found": True, "data": entreprise_info})
    
    
def prediagnostique_page(request):
    return render(request, "prediagnostic.html")

def homepage(request):
    return render(request, "home.html" )
