import time 
import requests
from django.conf import settings
from django.core.cache import cache 

TOKEN_CACHE_KEY = "insee_api_token"
TOKEN_TTL_MARGIN = 10 #si token < 10s, on le renouvelle automatiquement

def _recup_token_insee(): #privé, interne au module
    token_url = "https://api.insee.fr/token"  #INSEE utilise OAuth2, endpoint d'authentification
    data = {"grant_type": "client_credentials"} 
    reponse  = requests.post(token_url, data=data, auth=(settings.API_CLIENT_ID, settings.API_CLIENT_SECRET), timeout=10)
    reponse.raise_for_status()
    return reponse.json

"""
    Retourne un token valide (mis en cache pour éviter
    un appel au serveur INSEE à chaque requête).
    """
def get_insee_token():
    # 1. On regarde si un token existe déjà dans le cache
    cached = cache.get(TOKEN_CACHE_KEY)
    if cached:
        # Le token n’est pas expiré → on l’utilise directement
        return cached["access_token"]
    else:
        # 2. Aucun token valide → on en demande un nouveau à l’INSEE
        data = _recup_token_insee()
        access_token = data.get("access_token")
        expires_in = data.get("expires_in", 3600)# durée de vie du token en secondes (1h)

# 3. On garde une marge pour éviter d'utiliser un token expiré
    ttl = max(0, int(expires_in) - TOKEN_TTL_MARGIN)
     
# 4. On stocke le nouveau token en cache pour toutes les futures requêtes
    cache.set(TOKEN_CACHE_KEY, {"access_token": access_token}, timeout=ttl)
    
    return access_token

# Déclare une fonction qui prend en entrée un numéro SIRET (14 chiffres).

def verify_siret(siret):
    token = get_insee_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.insee.fr/entreprises/sirene/V3/siret/{siret}"
    resp = requests.get(url, headers=headers, timeout=10) 
    # On envoie la requête HTTP vers l’INSEE. 1) headers contient le token, 
    # 2)timeout=10 évite que ton serveur reste bloqué trop longtemps 
    # 3) resp est la réponse (HTML, JSON, erreur, etc…)
    if resp.status_code == 401 : 
    # token possiblement expiré : on efface le cache et retente une fois
        cache.delete(TOKEN_CACHE_KEY)
        token = get_insee_token()
        # Header obligatoire pour appeler l'API INSEE
        headers = {"Authorization": f"Bearer {token}"}
        # URL officielle pour récupérer les infos d'un SIRET
        url = f"https://api.insee.fr/entreprises/sirene/V3/siret/{siret}"
        resp = requests.get(url, headers=headers, timeout=10) 
    else :
        resp.raise_for_status()
        return resp.json()





    
