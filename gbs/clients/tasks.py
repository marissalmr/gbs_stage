from datetime import timedelta
from django.utils import timezone as dj_timezone
from celery import shared_task
from django.conf import settings

from .models import RendezVous
from django.core.mail import send_mail


@shared_task
def send_rdv_reminders():
    now = dj_timezone.now()
    # Liste des offsets : 2 jours avant et jour même
    #un offset est un décalage par rapport à une date de référence.
    offsets = [2, 0]

    for offset in offsets:
        target_date = now + timedelta(days=offset)
        
        if offset == 2:
        # J-2 → on ne prend que les RDV pour lesquels le rappel n'a pas encore été envoyé
            rdvs = RendezVous.objects.filter(
                start__date=target_date.date(),
                reminder_sent=False
            )
        else:
                # J-0 → on prend tous les RDV du jour même
            rdvs = RendezVous.objects.filter(
                start__date=target_date.date()
    )
            
                
        
    

    for rdv in rdvs:
        print(f"📨 Envoi email à {rdv.contact.email} (offset {offset})")  # log pour tester

        send_mail(
            subject="Rappel de votre rendez-vous",
            message=f"""
Bonjour {rdv.contact.nom},

Petit rappel : votre rendez-vous est prévu le
{rdv.start.strftime('%d/%m/%Y à %H:%M')}

À très bientôt.
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[rdv.contact.email],
            fail_silently=False
        )
        if offset == 2:
            rdv.reminder_sent = True
            rdv.save()