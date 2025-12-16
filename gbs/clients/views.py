from django.http import JsonResponse
from django.shortcuts import redirect, render
from .forms import *
from .api import *
from .models import *
import json
from .questions import *

def clean_siret(self):
    siret = self.cleaned_data['siret']
    if len(siret)!=14 or not siret.isdigit() :
        raise forms.ValidationError("Le SIRET doit contenir 14 chiffres.")
    
def prediag_view(request):
    if request.method == "POST" : 
        form = PrediagForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect("thanks")
    else:
        form = PrediagForm()
    
    questions_json = json.dumps((QUESTIONS_DIAG))
    return render(request, "clients/prediagnostic.html", {"form": form, "question_json" : questions_json})

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
        print("JSON INSEE : ", data)


    # 4. Tout s'est bien passé → on renvoie les données    
    except Exception as e:
        
    # 5. Si INSEE renvoie une erreur, token expiré, mauvais siret, etc.
    # On informe le front avec valid=False

        return JsonResponse(
            {"valid": False, "error": str(e)},
            status=400  # encore une erreur due à la requête
        )
    
    etab = data["etablissement"]
    unite = etab["uniteLegale"]
    
    entreprise_info = {
        "siret": etab.get("siret"),
        "siren": etab["siret"][:9],

        "date_creation": unite.get("dateCreationUniteLegale"),
        "statut_admin": unite.get("etatAdministratifUniteLegale"),
        "nom_officiel": unite.get("denominationUniteLegale"),
        "autres_noms": ", ".join([
                unite.get("denominationUsuelle1UniteLegale") or "",
                unite.get("denominationUsuelle2UniteLegale") or "",
                unite.get("denominationUsuelle3UniteLegale") or ""  
                ]),
        "prenom_dirigeant": ", ".join([
                unite.get("prenom1UniteLegale") or "",
                unite.get("prenom2UniteLegale") or "",
                unite.get("prenom3UniteLegale") or "",
                unite.get("prenom4UniteLegale") or ""
            ])
        }
    Client.objects.update_or_create(
        siret= entreprise_info["siret"],
         
         defaults={
        "date_creation": entreprise_info["date_creation"],
        "statut_admin": entreprise_info["statut_admin"],
        "nom_officiel": entreprise_info["nom_officiel"],
        "autres_noms": entreprise_info["autres_noms"],
        "prenom_dirigeant": entreprise_info["prenom_dirigeant"],
    }
    )
    return JsonResponse({"found": True, "data": entreprise_info})
    
    
def prediagnostique_page(request):
    form = ClientForm()
    return render(request, "prediagnostic.html", {"form": form})

def homepage(request):
    return render(request, "home.html" )

def formulaire_client(request):
    if request.method == "POST" :
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("thanks")
        else : 
            form = ClientForm()
        return render(request, "clients/prediagnostic.html", {"form": form})

def start_diag(request, client_id):

    client = Client.objects.get(id=client_id)
    dossier_client = Dossiers.objects.create(
        client = client,
        type_dossier = '',
        statut = 'en_attente',)
    
    return redirect(request, "clients/prediagnostic.html", dossier_client = dossier_client.id, question_number =1 ) 
    
    