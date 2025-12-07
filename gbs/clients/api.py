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
def get_api_token():
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

    
