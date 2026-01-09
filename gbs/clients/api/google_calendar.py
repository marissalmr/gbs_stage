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

#Fonction qui va vérifier si un créneau est libre
def is_available(start_rdv, duration_minutes=60):
    service = get_calendar_service()
    end_rdv = start_rdv + timedelta(minutes=duration_minutes)
    events = service.events().list(  #demande à google calendar tous les events entre start_rdv et fin_rdv
        calendarId=settings.GOOGLE_CALENDAR_ID, 
        #On regarde dans le calendrier du tuteur
        timeMin=start_rdv.isoformat(), 
        timeMax=end_rdv.isoformat(),
        singleEvents=True
    ).execute() #Envoie la requete à Google et récupere les events

    return len(events.get("items", [])) == 0 #liste des événements trouvés dans ce créneau.
                                            # Si la liste est vide le créneau est libre, on renvoie True.


def show_if_rdv_available(date):
    service = get_calendar_service()

    start_day = datetime.combine(date, datetime.min.time())
    end_day = start_day + timedelta(days=1)
    #Plage analysée : [ 10/01 00:00  →  11/01 00:00 ]

    events = service.events().list(  #Donne moi les évents de cette plage
        calendarId=settings.GOOGLE_CALENDAR_ID, 
        timeMin=start_day.isoformat(), 
        timeMax=end_day.isoformat(),
        singleEvents=True
    ).execute() #Envoie la requete à Google et récupere les events
    heure_reserver = []
    for evenements in events.get("items", []): #Items = liste évenements google
        start = evenements.get("start",{}).get("dateTime") #Récup heure début évenements
        if start:
            dt = datetime.fromisoformat(start.replace("Z", ""))
            heure_reserver.append(dt.strftime("%H:%M"))
            return heure_reserver






