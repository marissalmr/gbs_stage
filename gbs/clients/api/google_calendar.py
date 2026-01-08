from google.oauth2 import service_account  #Gère l’authentification service account, Lit fichier JSON ,Crée une identité serveur reconnue par Google
from googleapiclient.discovery import build
from django.conf import settings
from datetime import datetime, timedelta #timedelta permet d'ajouter h+1


SCOPES =  ["https://www.googleapis.com/auth/calendar.events"]
#Permission de lire et ajouter des rdv

def get_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    ) # 3. On crée la connexion officielle avec Google
    # On précise qu'on veut le service 'calendar', en version 'v3'
    # On lui donne nos credentials (la preuve qu'on a le droit d'être là)

    return build('calendar', 'v3', credentials=credentials)

def test_google_auth():
    service = get_calendar_service()
    return service is not None

def create_event(titre,description, start_rdv, duration_minutes=60):

    service = get_calendar_service() 
    #On récupère le client Google, Authentifié, Prêt à parler à l’API
    end_rdv = start_rdv + timedelta(minutes=duration_minutes)
    #On calcule la fin du rdv 
    event = {
        "summary": titre,
        "description" : description,
        "start": {
            "dateTime": start_rdv.isoformat(),
            "timeZone": "Europe/Paris",
        },
        "end": {
            "dateTime": end_rdv.isoformat(),
            "timeZone": "Europe/Paris",
        },
    }
    created_event = service.events().insert(
    calendarId=settings.GOOGLE_CALENDAR_ID,
    body=event
).execute()
    #Appelle Google Calendar API, insère l’événement, le bloque 
    return created_event

