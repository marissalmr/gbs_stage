from django.contrib import admin
from .models import Contact, Dossiers, Documents, Prediagnostique, Question, Reponse, Entreprise

admin.site.register(Contact)
admin.site.register(Dossiers)
admin.site.register(Documents)
admin.site.register(Prediagnostique)
admin.site.register(Entreprise)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['code', 'texte_question', 'type']

@admin.register(Reponse)
class ReponseAdmin(admin.ModelAdmin):
    list_display = ['dossier','contact', 'question', 'reponse_user']
 
#Pour voir les données enregistrés
# Register your models here.
