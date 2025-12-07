import time 
import requests
from django.conf import settings
from django.core.cache import cache 

TOKEN_CACHE_KEY = "insee_api_token"
TOKEN_TTL_MARGIN = 10 #si token < 10s, on le renouvelle automatiquement

def _recup_token_insee(): #privé, interne au module
    token_url = "https://api.insee.fr/token"  #INSEE utilise OAuth2, endpoint d'authentification
    data = {"grant_type": "client_credentials"} #
    reponse  = requests.post(token_url, data=data, auth=(settings.API_CLIENT_ID, settings.API_CLIENT_SECRET), timeout=10)
    reponse.raise_for_status()
    return reponse.json
