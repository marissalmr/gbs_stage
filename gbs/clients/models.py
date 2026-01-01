from django.db import models

class Entreprise(models.Model):
    siret = models.CharField(max_length=14, unique=True)
    date_creation = models.DateField(blank=True, null=True)
    statut_admin = models.CharField(max_length=250, blank=True, null=True)
    nom_officiel = models.CharField(max_length=90, blank=True, null=True)
    autres_noms = models.TextField(max_length=250, blank=True, null=True)
    prenom_dirigeant = models.CharField(max_length=200, blank=True, null=True)

class Contact(models.Model):
    nom = models.CharField(max_length=200)
    email = models.CharField(max_length=300)
    telephone = models.CharField(max_length=50)
    adresse = models.CharField(max_length=200)
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=5)
    
types_dossiers_choices = [
        ('QUALIBAT', 'QUALIBAT'),
        ('QUALIT_ENR', 'QUALIT’ENR'),
        ('AEAO', 'AUDIT ENERGETIQUE AFNOR & OPQIBI'),
        ('CERTIBAT', 'CERTIBAT'),
        ('QUALIF_ELEC', 'QUALIF’ELEC'),
        ('AMO', 'Accompagnateur Rénov'),
    ]

class Dossiers(models.Model):
    contact = models.ForeignKey(
        Contact, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True)
    
    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name="dossiers"
    )
    
    type_dossier = models.CharField(max_length=50, choices=types_dossiers_choices)
    statut_choices = [
        ('en_attente', 'En attente'),
        ('Incomplet' , 'Incomplet'),
        ('validé', 'Validé'),
    ]
    statut = models.CharField(max_length=30,choices=statut_choices, default="en_attente")
    eligibilite_estimee = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

class Documents(models.Model):
    dossier = models.ForeignKey(Dossiers, on_delete=models.CASCADE,related_name='documents'),
    nom = models.CharField(max_length=150),
    type = models.CharField(max_length=150),


class Question(models.Model):
    code = models.CharField(max_length=200,)
    texte_question = models.TextField()
    
    type = models.CharField( #Définit comment l’utilisateur peut répondre
        max_length=10,
        choices=[
                ("single", "Choix unique"),
                ("multiple", "Choix multiple"),
                ]
)
    choices = models.JSONField(default=list)
    
    
class Reponse(models.Model):
    dossier = models.ForeignKey(
        Dossiers,
        on_delete=models.CASCADE,
        related_name="responses"
    )
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="reponses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="reponses")
    reponse_user = models.JSONField()


class Prediagnostique(models.Model):
    dossier = models.ForeignKey(Dossiers, on_delete=models.CASCADE,related_name='documents'),
    reponse = models.TextField()
    sous_traitee = models.BooleanField(default=False)
    score = models.IntegerField(null=True, blank=True)









