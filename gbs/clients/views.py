from django.http import JsonResponse
from django.shortcuts import redirect, render
from .forms import *
from .api.insee import verify_siret
from .models import *
import json
from datetime import datetime
from django.db import IntegrityError


#Sert à : - récupérer le SIRET 
# -créer / mettre à jour le contact
# -stocker contact_id en session   
def prediag_view(request):
    if request.method == "POST" :
        siret = request.POST.get("siret")
        contact = Contact.objects.filter(dossiers__entreprise__siret=siret).first()
        form = ClientForm(request.POST, instance=contact) 
        if form.is_valid():
            contact = form.save(commit=False)
            request.session["contact_id"] = contact.id
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
    return JsonResponse({"found": True, "data": entreprise_info})

def save_contact(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        data = json.loads(request.body)
        date_creation = data.get("date_creation")

        if Contact.objects.filter(email=data["email"]).exists():
            return JsonResponse(
                {"error": "Cet email a déjà été utilisé pour un dossier"},
                status=400
            )

        if date_creation:
            date_creation = datetime.strptime(date_creation, "%Y-%m-%d").date()

        entreprise, _ = Entreprise.objects.update_or_create(
            siret=data["siret"],
            defaults={
                "nom_officiel": data.get("nom_officiel"),
                "date_creation": date_creation,
                "statut_admin": data.get("statut_admin"),
                "autres_noms": data.get("autres_noms"),
                "prenom_dirigeant": data.get("prenom_dirigeant"),
            }
        )

        contact, _ = Contact.objects.update_or_create(
            email=data["email"],
            defaults={
                "nom": data["nom"],
                "telephone": data["telephone"],
                "adresse": data["adresse"],
                "ville": data["ville"],
                "code_postal": data["code_postal"],
            }
        )

        dossier, _ = Dossiers.objects.get_or_create(
            contact=contact,
            entreprise=entreprise,
            type_dossier="QUALIBAT"
        )

        request.session["contact_id"] = contact.id
        request.session["entreprise_id"] = entreprise.id
        request.session["dossier_id"] = dossier.id

        return JsonResponse({"success": True})

    except IntegrityError:
        return JsonResponse({"error": "Conflit base de données"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def prediagnostique_page(request):
    form = ClientForm()
    return render(request, "prediagnostic.html", {"form": form})

def homepage(request):
    return render(request, "home.html" )


def questionnaire(request):
    # On récupère toutes les questions en base
    questions = Question.objects.all()

    if request.method == "POST":
         # On recrée le formulaire AVEC les données envoyées + liste questions
        form = QuestionnaireForm(request.POST, questions=questions)
        if form.is_valid(): 
             # On parcourt toutes les réponses du formulaire
            for question_id, reponse in form.cleaned_data.items():
                # On récupère la question correspondante
                question = Question.objects.get(id=question_id)
                contact = Contact.objects.get(id=request.session.get("contact_id"))

                Reponse.objects.create(
                    contact = contact,
                    question = question,
                    reponse_user = reponse

                )
                
            return redirect("success")
                
    else:
        form = QuestionnaireForm(questions=questions)
        return render(request, "questionnaire_eligibilite.html", {"form": form})

def api_questions(request):
    questions = Question.objects.all()
    data = []

    for q in questions:
        data.append({
            "id": q.id,
            "code": q.code,
            "text": q.texte_question,
            "type": q.type,           # single / multiple
            "options": q.choices      # JSON list directement
        })

    return JsonResponse({"questions": data})

def save_answer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        contact_id = request.session.get("contact_id")
        if not contact_id:
            return JsonResponse({"error":"Contact non trouvé en session"}, status=400)

        contact = Contact.objects.get(id=contact_id)
        question = Question.objects.get(id=data["question_id"])

        # On récupère le dossier
        dossier = Dossiers.objects.filter(contact=contact).first()

        Reponse.objects.create(
            dossier=dossier,
            contact=contact,
            question=question,
            reponse_user=data["answer"]
        )
        return JsonResponse({"success": True})
    return JsonResponse({"error":"Invalid request"}, status=400)

def submit_final(request):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    try:
        data = json.loads(request.body)

        # 👉 ici tu as TOUT :
        # data["siret"]
        # data["entrepriseData"]
        # data["contact"]
        # data["answers"]

        # TODO : sauvegarde DB / CRM / email / webhook

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)