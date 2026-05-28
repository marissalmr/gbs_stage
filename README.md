GBS – Plateforme de gestion des certifications RGE (QUALIBAT / QUALIT'ENR / QUALIFELEC)

L’application permet de gérer un parcours complet d’accompagnement aux certifications pour les entreprises du BTP :

vérification du SIRET via l’API INSEE,
création automatique de contacts et dossiers,
questionnaire d’éligibilité dynamique,
sauvegarde des réponses en base de données,
prise de rendez-vous via Google Calendar,
envoi d’emails récapitulatifs automatiques,
gestion des propositions de disponibilité.
Pourquoi Django ?

J’ai choisi Django car je maîtrisais déjà Python et je voulais comprendre le fonctionnement d’un framework web.

Cela m’a permis de :

comprendre l’architecture MVT,
gérer une base de données relationnelle,
créer des vues et des APIs JSON,
utiliser les sessions utilisateur,
intégrer des services externes comme Google Calendar et l’API INSEE.
Défis rencontrés

J’ai rencontré plusieurs difficultés techniques :

gestion des sessions entre les différentes étapes du parcours,
intégration de l’API INSEE pour la vérification des SIRET,
synchronisation avec Google Calendar,
gestion des doublons (contacts, dossiers, rendez-vous),
structuration des données du questionnaire.

Ces problèmes m’ont permis de mieux comprendre la logique backend et la structure d’une application Django complète.

Pistes d’évolution

Voici quelques fonctionnalités que j’aimerais ajouter à l’avenir :

ajout d’un dashboard administrateur,
authentification utilisateur,
API REST complète avec Django REST Framework,
refonte frontend avec React ou Vue.js,
système de devis automatisé,
suivi avancé des dossiers.
Comment installer et exécuter le projet

Voici les étapes pour installer et lancer le projet en local.

Étapes d’installation

Cloner le projet

git clone <URL_DU_REPO>
cd gbs_stage

Créer et activer un environnement virtuel

python -m venv env

# macOS / Linux
source env/bin/activate

# Windows
env\Scripts\activate
Installer les dépendances
pip install -r requirements.txt
Créer la base de données
python manage.py migrate
Lancer le serveur en local
python manage.py runserver
Accès à l’application
http://127.0.0.1:8000/

Une fois le serveur lancé :

http://127.0.0.1:8000/
