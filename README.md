

GBS – Plateforme de gestion des certifications RGE pour les entreprises du BTP

Présentation du projet

L’application GBS est une plateforme web permettant d’accompagner les entreprises dans leurs démarches de certification (QUALIBAT, QUALIT’ENR, QUALIFELEC).

Elle permet de gérer un parcours complet :

vérification du SIRET via l’API INSEE
création automatique de contacts et dossiers
questionnaire d’éligibilité
stockage des réponses en base de données
prise de rendez-vous via Google Calendar
envoi d’un récapitulatif par email
gestion des disponibilités proposées par l’utilisateur
Pourquoi Django ?

J’ai choisi Django car je maîtrisais déjà Python et je voulais comprendre comment fonctionne un framework web.

Ce projet m’a permis de :

comprendre l’architecture MVT
gérer une base de données relationnelle
créer des vues et API JSON
manipuler les sessions utilisateur
intégrer des services externes (INSEE, Google Calendar, SMTP)
Défis rencontrés

J’ai rencontré plusieurs difficultés :

gestion des sessions entre les étapes du parcours
intégration de l’API INSEE pour les SIRET
synchronisation avec Google Calendar
gestion des doublons (dossiers, rendez-vous, contacts)
structuration des réponses du questionnaire

Ces difficultés m’ont permis de progresser sur la logique backend et la structuration d’un projet Django complet.

Fonctionnalités principales
Vérification de SIRET (API INSEE)
Création automatique de dossiers clients
Questionnaire dynamique
Sauvegarde des réponses en base de données
Prise de rendez-vous via Google Calendar
Vérification de disponibilité des créneaux
Envoi d’emails récapitulatifs automatiques
Gestion des propositions de créneaux hors calendrier
Installation et exécution du projet

Voici les étapes pour installer et lancer le projet en local.

1. Cloner le projet
git clone https://github.com/marissalmr/recettes.git
cd gbs_stage
2. Créer un environnement virtuel
python -m venv env

Activation :

# macOS / Linux
source env/bin/activate

# Windows
env\Scripts\activate
3. Installer les dépendances
pip install -r requirements.txt
4. Appliquer les migrations
python manage.py migrate
5. Lancer le serveur
python manage.py runserver
Accès à l’application

Une fois le serveur lancé :

http://127.0.0.1:8000/
