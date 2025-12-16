ACTIVITES_CHOICES = [
    ("isolation_exterieur", "Isolation extérieure / Ravalement"), #valeur_stockée, texte_affiché
    ("isolation_interieur", "Isolation intérieure / Projection / Flocage / Soufflage"),
    ("menuiserie_exterieure", "Menuiserie extérieure (fenêtres, Velux, portes)"),
    ("couverture_isolation_toiture", "Couverture et isolation sous toiture"),
    ("maconnerie_gros_oeuvre", "Maçonnerie - Gros œuvre – Béton "),
    ("etancheite", "Étanchéité"),
    ("carrelage_sol_pvc", "Carrelage / Sol PVC"),
    ("platrerie_cloison", "Plâtrerie / Cloisons / Placoplatre"),
    ("pac_vmc", "Pompe à chaleur / VMC"),
    ("photovoltaique", "Panneaux photovoltaïques"),
    ("chauffage", "Chauffage solaire / bois / gaz"),
    ("irve", "IRVE (bornes de recharge électrique)"),
    ("electricite", "Métier de l’électricité"),
    ("autres", "Autres")
     ]

CA_CHOICES = [
    ("<100k", "Moins de 100 000 €"),
    ("100k-250k", "Entre 100 000 € et 250 000 €"),
    ("250k-500k", "Entre 250 000 € et 500 000 €"),
    ("500k-1M", "Entre 500 000 € et 1 million €"),
    ("1M-2M", "Entre 1 et 2 millions €"),
    ("2M-5M", "Entre 2 et 5 millions €"),
    (">5M", "Plus de 5 millions €"),
]


QUESTIONS_DIAG = [
    {
        "id": 1,
     "question" :  "Que voulez-vous qualifier ?", 
     "choices": ACTIVITES_CHOICES, 
     "type": "multiple",
     },

    {
        "id": 2,
        "question": "Les activités que vous souhaitez qualifier sont-elles sous-traitées ?",
        "choices":
        [
            ("oui", "Oui"),
            ("non", "Non"),
        ],
        "type" : "single",
       
    }, 

    {
        "id": 3,
      "question": "Environ quel pourcentage de cette activité confiez-vous à des sous-traitants ?",
        "choices": [
            ("<25", "Moins de 25 %"),
            ("25-50", "Entre 25 % et 50 %"),
            ("50-75", "Entre 50 % et 75 %"),
            (">75", "Plus de 75 %"),
            ("100", "100 % sous-traité"),
                    ], 
            "type" : "single",
            "show_if": {
                        "question_id" : 2,
                        "value" : "oui",
                        }       
            },
    {
        "id": 4,
        "question" :  "Quel est votre chiffre d’affaires annuel approximatif ?", 
        "choices": CA_CHOICES,
        "type": "single",
        "show_if" : {
                    "question_id" : 2,
                    "value" : "non",
                    }

     },

     {
        "id": 5,
     "question" :  "Avez-vous déjà réglé des frais de dossier ou un bon de commande auprès de QUALIBAT en 2025 ?", 
     "choices":[
        
         ("oui", "Oui"),
         ("non", "Non"),
                ], 
        "type" : "single",
     },

     {
        "id": 6,
     "question" :  "Avez-vous déjà suivi une formation RENOV’PERF (transverse et/ou modules métiers) ?", 
     "choices": [
        
         ("oui", "Oui"),
         ("non", "Non"),
        
                ], 
        "type" : "single",
     },
     
     {
        "id": 7,
     "question" :  "Combien d’ouvriers interviennent habituellement sur vos chantiers ?", 
     "choices": [
        
            ("moins_10", "Moins de 10 ouvriers"),
            ("plus_10", "10 ouvriers ou plus"),
        
                ],  
        "type" : "single",
     },

     {
        "id": 8,
     "question" :  "Combien de chantiers de fourniture et pose d’isolants avez-vous déjà réalisés pour ces activités ?", 
     "choices": [
         
            ("0_2", "Moins de 3 chantiers"),
            ("3_plus", "3 chantiers ou plus"),
            
                ],
            "type" : "single",
     },
  
    ],
    
    

