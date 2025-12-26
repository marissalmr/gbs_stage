from django.contrib import admin
from .models import Client, Dossiers, Documents, Prediagnostique, Question, Reponse

admin.site.register(Client)
admin.site.register(Dossiers)
admin.site.register(Documents)
admin.site.register(Prediagnostique)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['code', 'texte_question', 'type']

@admin.register(Reponse)
class ReponseAdmin(admin.ModelAdmin):
    list_display = ['client', 'question', 'reponse_user']
 
#Pour voir les données enregistrés
# Register your models here.
