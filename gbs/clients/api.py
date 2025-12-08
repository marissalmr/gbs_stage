import time 
import requests
from django.conf import settings
from django.core.cache import cache 

INSEE_API_KEY = "f69b8319-7e20-47a8-9b83-197e2037a8e5"


def verify_siret(siret):
    siret_clean = siret.replace(" ", "")  # retire les espaces
    url = f"https://api.insee.fr/api-sirene/3.11/siret/{siret_clean}"
    headers = {"X-INSEE-Api-Key-Integration": INSEE_API_KEY}

    resp = requests.get(url, headers=headers, timeout=10)
    
    if resp.status_code == 404:
        raise ValueError(f"SIRET {siret_clean} introuvable.")
    
    resp.raise_for_status()  # lève exception pour autres erreurs
    return resp.json()  