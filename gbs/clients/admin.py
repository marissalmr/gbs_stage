from django.contrib import admin
from .models import Client, Dossiers, Documents, Prediagnostique

admin.site.register(Client)
admin.site.register(Dossiers)
admin.site.register(Documents)
admin.site.register(Prediagnostique)
 
#Pour voir les données enregistrés
# Register your models here.
