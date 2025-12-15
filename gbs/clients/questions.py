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
        "show_if": {
            "question_id" : 2,
            "question_choices" : "oui",
        }
    }, 
    {"id": 3,
      "question": "Environ quel pourcentage de cette activité confiez-vous à des sous-traitants ?",
        "choices": [
            ("<25", "Moins de 25 %"),
            ("25-50", "Entre 25 % et 50 %"),
            ("50-75", "Entre 50 % et 75 %"),
            (">75", "Plus de 75 %"),
            ("100", "100 % sous-traité"),
            ],        
            },
            
    ],
    
    

