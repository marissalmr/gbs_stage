from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
import pytz
from .forms import *
from clients.api.google_calendar import get_calendar_service
from .api.insee import verify_siret
from .models import *
import json
from datetime import datetime
from django.db import IntegrityError
from clients.api.google_calendar import (
    is_available,
    create_event
)
from clients.api.google_calendar import show_if_rdv_available
from django.core.mail import send_mail
from .models import Reponse
from .service import api_error
from .service import api_method_not_allowed
from .models import Disponibilite_rdv


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
        return api_error("SIRET manquant")
    
    if Dossiers.objects.filter(entreprise__siret=siret).exists():
       return api_error("Ce SIRET a déjà rempli le questionnaire")

   
    try : 
        data = verify_siret(siret)
        
    # 4. Tout s'est bien passé → on renvoie les données    
    except Exception as e:
        
    # 5. Si INSEE renvoie une erreur, token expiré, mauvais siret, etc.
    # On informe le front avec valid=False
       return api_error("SIRET invalide ou introuvable")
    
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
       return api_method_not_allowed("Méthode non autorisée")
    try:
        data = json.loads(request.body)
        date_creation = data.get("date_creation")

        if date_creation:
            date_creation = datetime.strptime(date_creation, "%Y-%m-%d").date()

        defaults = {
            "date_creation": date_creation,
            "statut_admin": data.get("statut_admin"),
            "autres_noms": data.get("autres_noms"),
            "prenom_dirigeant": data.get("prenom_dirigeant"),
        }

        if data.get("nom_officiel"):
            defaults["nom_officiel"] = data["nom_officiel"]

        entreprise, _ = Entreprise.objects.update_or_create(
            siret=data["siret"],
            defaults=defaults
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

        dossier, created = Dossiers.objects.get_or_create(
            entreprise=entreprise,
                defaults={
                    "contact": contact,
                    "type_dossier": "QUALIBAT"
                }
        )

# Si le dossier existe déjà, on met à jour le contact
        if not created:
            dossier.contact = contact
            dossier.save()

        request.session["contact_id"] = contact.id
        request.session["entreprise_id"] = entreprise.id
        request.session["dossier_id"] = dossier.id

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def prediagnostique_page(request):
    form = ClientForm()
    return render(request, "prediagnostic.html", {"form": form})

def homepage(request):
    return render(request, "home.html" )


def questionnaire(request):
       return render(request, "questionnaire_eligibilite.html")

def api_questions(request):
    questions = Question.objects.order_by("code")
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
            return api_error("Utilisateur non identifié")

        contact = Contact.objects.get(id=contact_id)
        question = Question.objects.get(id=data["question_id"])

        # On récupère le dossier
        dossier_id = request.session.get("dossier_id")
        dossier = Dossiers.objects.get(id=dossier_id)
        

        Reponse.objects.create(
            dossier=dossier,
            contact=contact,
            question=question,
            reponse_user=data["answer"]
        )

        print("contact_id:", contact_id)
        print("dossier_id:", dossier_id)
        print("question_id:", data["question_id"])
        print("answer:", data["answer"])

        return JsonResponse({"success": True})
    return api_error("Certains champs n'ont pas été remplis")

def send_mail_summary(dossier):
    entreprise = dossier.entreprise
    contact = dossier.contact
    reponses = dossier.responses.select_related("question")

    recap_mail = "Nouvelle soumission de questionnaire\n\n"
    recap_mail += f"SIRET : {entreprise.siret}\n"
    recap_mail += f"Entreprise : {entreprise.nom_officiel}\n\n"

    recap_mail += "Contact\n"
    recap_mail += f"Nom : {contact.nom}\n"
    recap_mail += f"Email : {contact.email}\n"
    recap_mail += f"Téléphone : {contact.telephone}\n\n"

    recap_mail += "Réponses au questionnaire\n\n"

    for rep in reponses:
        question = rep.question.texte_question
        answer = rep.reponse_user  # JSONField → déjà Python object

        # Transformer tout en string lisible
        if isinstance(answer, list):
            answer = ", ".join(str(a) for a in answer)
        elif isinstance(answer, dict):
            # si tu as des dict (ex: {option: True/False})
            answer = ", ".join(f"{k}: {v}" for k, v in answer.items())
        else:
            answer = str(answer)

        if not answer:
            answer = "—"

        recap_mail += f"- {question}\n"
        recap_mail += f"  ➜ {answer}\n\n"

    send_mail(
        subject="Nouvelle demande – Questionnaire GBS",
        message=recap_mail,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["marielnrtstu@gmail.com"],
        fail_silently=False,
    )


def submit_final(request):
    if request.method != "POST":
        return api_method_not_allowed()
    try:
        dossier_id = request.session.get("dossier_id")
        if not dossier_id:
            return api_error("Dossier introuvable")
        
        dossier = Dossiers.objects.select_related(
            "entreprise",
            "contact"
        ).get(id=dossier_id)

        send_mail_summary(dossier)

        return JsonResponse({"success": True})
    
    except Exception as e:
        return api_error("Erreur lors de l'envoi du récapitulatif")

    
def book_appointment(request):
    if request.method != "POST":
        return api_method_not_allowed()
    data = json.loads(request.body.decode("utf-8"))
    
    tz = pytz.timezone("Europe/Paris")
    start_rdv = datetime.fromisoformat(data["start_rdv"])
    if start_rdv.tzinfo is None:
        start_rdv = tz.localize(start_rdv)
    else:
        start_rdv = start_rdv.astimezone(tz)


    # 1️⃣ Interdire les dates passées
    now = datetime.now(pytz.timezone("Europe/Paris"))
    if start_rdv < now:
        return api_error("Impossible de réserver un créneau passé")

    # 2️⃣ Vérifier disponibilité Google Calendar
    if not is_available(start_rdv):
        return api_error("Ce créneau n'est plus disponible")
    # 3️⃣ Récupération du contact
    contact_id = request.session.get("contact_id")
    if not contact_id:
       return api_error("Utilisateur non identifié")
    contact = Contact.objects.get(id=contact_id)

    # 4️⃣ Vérifier si le contact a déjà un RDV
    service = get_calendar_service()
    events = service.events().list(
        calendarId=settings.GOOGLE_CALENDAR_ID,
        q=contact.email,
        singleEvents=True
    ).execute()

    if events.get("items"):
       return api_error("Vous avez déjà un rendez-vous programmé")
    
    print("RDV envoyé à Google :", start_rdv, start_rdv.tzinfo)

    # 5️⃣ Création du RDV
    event = create_event(
        titre=f"RDV client : {contact.nom}",
        description=f"Rendez-vous pris par {contact.nom} ({contact.email})",
        start_rdv=start_rdv
    )

    RendezVous.objects.create(
            contact=contact,
            start=start_rdv,
            google_event_id=event.get('id'),
            reminder_sent = False
        )

    return JsonResponse({
        "success": True,
        "message": "Rendez-vous créé avec succès",
        "event_id": event.get("id"),
        "start": start_rdv.isoformat()
    }, status=201)


def get_booked_times_for_day(request):
    """
    API endpoint Django pour retourner les créneaux horaires déjà réservés 
    Utilisé côté frontend pour griser les créneaux indisponibles.
    """

    #Récupère la date depuis les paramètres GET 
    date_str = request.GET.get("date")  

    #Si pas de date fournie → on renvoie une erreur 400
    if not date_str:
       return api_error("Date manquante")
    #Convertit la date string en objet datetime.date
    date = datetime.fromisoformat(date_str).date()

    #Appelle la fonction backend pour récupérer les heures déjà réservées
    available_or_not = show_if_rdv_available(date)

    #Renvoie la liste des créneaux sous forme JSON au frontend
    return JsonResponse({"reserved": available_or_not})

def contact_homepage(request):
    if request.method != "POST":
        return api_method_not_allowed()
    try:
        data = json.loads(request.body)

        nom = data.get("nom")
        entreprise = data.get("entreprise")
        email = data.get("email")
        message = data.get("message")

        if not nom or not email or not message:
            return api_error("Tous les champs sont obligatoires")
        message_email = f"""
 Nouveau message depuis la homepage

Nom : {nom}
Entreprise : {entreprise}
Email : {email}

Message :
{message}
        """

        send_mail(
            subject="Nouveau message – Page Contact",
            message=message_email,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["marielnrtstu@gmail.com"],
            fail_silently=False,
        )

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

def propose_rdv(request):
    if request.method != "POST":
        return api_method_not_allowed("Méthode non autorisée")
    
    try:
        data = json.loads(request.body)
        contact_id = request.session.get("contact_id")
        dossier_id = request.session.get("dossier_id")

        if not contact_id or not dossier_id:
            return api_error("Utilisateur ou dossier non identifié")

        contact = Contact.objects.get(id=contact_id)
        dossier = Dossiers.objects.get(id=dossier_id)

        proposed_dt = datetime.fromisoformat(data["proposed_datetime"])
        tz = pytz.timezone("Europe/Paris")
        proposed_dt = tz.localize(proposed_dt)

        message = data.get("message", "")

        Disponibilite_rdv.objects.create(
            dossier=dossier,
            contact=contact,
            proposed_datetime=proposed_dt,
            message=message
        )

        return JsonResponse({"success": True, "message": "Votre proposition a été enregistrée"})
    
    except Exception as e:
        return api_error(f"Erreur : {str(e)}")



def propose_disponibilite(request):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    data = json.loads(request.body)

    date = data.get("date")
    time = data.get("time")

    if not date or not time:
        return JsonResponse({"error": "Date ou heure manquante"}, status=400)

    send_mail(
        subject=" Nouvelle disponibilité proposée",
        message=f"""
Un utilisateur a proposé une disponibilité hors créneaux standards.

Date souhaitée : {date}
Heure souhaitée : {time}

Merci de le recontacter rapidement.
""",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["marielnrtstu@gmail.com"],
        fail_silently=False
    )

    return JsonResponse({"success": True})