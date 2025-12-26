from django.core.management.base import BaseCommand
from clients.models import Question

QUESTIONS = [
    ("Q1", "Que voulez-vous qualifier ?", "multiple"),
    ("Q2", "Les activités sont-elles sous-traitées ?", "single"),
    ("Q3", "Pourcentage de sous-traitance ?", "single"),
    ("Q4", "Quel est votre chiffre d’affaires ?", "single"),
    ("Q5", "Avez-vous déjà payé QUALIBAT ?", "single"),
    ("Q6", "Avez-vous suivi une formation RENOV’PERF ?", "single"),
    ("Q7", "Combien d’ouvriers sur vos chantiers ?", "single"),
    ("Q8", "Combien de chantiers réalisés ?", "single"),
]

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for code, texte, type_question in QUESTIONS:
            Question.objects.create(
                code=code,
                texte_question=texte,
                type=type_question
            )

