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
    
    # 3. On appelle ta fonction qui contacte INSEE + gère token + cache

    try : 
        data = verify_siret(siret)
    # 4. Tout s'est bien passé → on renvoie les données
        return JsonResponse({"valid": True, "data": data})
    
    except Exception as e:

        # 5. Si INSEE renvoie une erreur, token expiré, mauvais siret, etc.
        # On informe le front avec valid=False
        return JsonResponse(
            {"valid": False, "error": str(e)},
            status=400  # encore une erreur due à la requête
        )

def prediagnostique_page(request):
    return render(request, "prediagnostic.html")