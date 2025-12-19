from django.http import JsonResponse
from django.shortcuts import redirect, render
from .forms import *
from .api import *
from .models import *
import json

def clean_siret(self):
    siret = self.cleaned_data['siret']
    if len(siret)!=14 or not siret.isdigit() :
        raise forms.ValidationError("Le SIRET doit contenir 14 chiffres.")
    
def prediag_view(request):
    if request.method == "POST" :
        siret = request.POST.get("siret")
        client = Client.objects.filter(siret=siret).first()
        form = ClientForm(request.POST, instance=client) 
        if form.is_valid():
            client = form.save(commit=False)
            form.save()
            return redirect("questionnaire")   
    else :
        form = ClientForm()
    return render(request, 'prediagnostic.html', {"form": form})


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
    siret = None 
    # Vérifie si le formulaire a été soumis en méthode POST
    if request.method == "POST":
        # Récupère le SIRET envoyé dans le formulaire
        siret = request.POST.get('siret')
    
    # Si un SIRET a été fourni, on cherche le client correspondant en base
    if siret:
        # filter() renvoie un QuerySet, .first() permet de récupérer le premier objet ou None
        client = Client.objects.filter(siret=siret).first()
    else:
        # Aucun SIRET fourni → pas de client existant
        client = None

    # Crée un formulaire Django avec les données POST
    # Si client existe, on va mettre à jour ce client (instance=client)
    # Sinon, on créera un nouveau client à l'enregistrement
    form = ClientForm(request.POST, instance=client)

    # Vérifie si les données du formulaire sont valides
    if form.is_valid():
        # Enregistre le client en base (nouveau ou mise à jour)
        form.save()
    else:
        # Si les données ne sont pas valides, réinitialise le formulaire vide
        form = ClientForm()

    # Affiche le template 'prediagnostic.html' avec le formulaire (mis à jour ou vide)
    return render(request, "prediagnostic.html", {"form": form})
def start_diag(request, client_id):

    client = Client.objects.get(id=client_id)
    dossier_client = Dossiers.objects.create(
        client = client,
        type_dossier = '',
        statut = 'en_attente',)
    
    return redirect(request, "prediagnostic.html", dossier_client = dossier_client.id, question_number =1 ) 
    
def questionnaire_page(request):
    return render(request, "questionnaire_eligibilite.html")