from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings

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



