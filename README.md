# GBS – Plateforme de gestion des certifications RGE

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-5.1-darkgreen)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)


## Présentation du projet

GBS est une application web développée avec Django permettant de gérer un parcours complet d’accompagnement aux certifications RGE pour les entreprises du BTP :

* QUALIBAT
* QUALIT'ENR
* QUALIFELEC

L’objectif du projet est de centraliser et automatiser les différentes étapes administratives liées aux certifications.

---

## Fonctionnalités principales

L’application permet notamment de :

* Vérifier automatiquement un numéro SIRET via l’API INSEE,
* Créer automatiquement des contacts et dossiers,
* Générer un questionnaire d’éligibilité dynamique,
* Sauvegarder les réponses en base de données,
* Proposer des disponibilités de rendez-vous,
* Synchroniser les rendez-vous avec Google Calendar,
* Envoyer des emails récapitulatifs automatiques,
* Gérer les doublons de contacts, dossiers et rendez-vous.

---

## Pourquoi Django ?

J’ai choisi Django car je maîtrisais déjà Python et je souhaitais approfondir ma compréhension du développement web backend à travers un framework complet.

Ce projet m’a permis de travailler sur plusieurs notions importantes :

* l’architecture MVT,
* la gestion d’une base de données relationnelle,
* les vues Django et les APIs JSON,
* la gestion des sessions utilisateur,
* l’intégration de services externes,
* la structuration logique d’une application web complète.

J’ai également découvert des problématiques concrètes rencontrées dans des projets métier réels.

---

## Défis rencontrés

Plusieurs difficultés techniques ont été rencontrées durant le développement :

* gestion des sessions entre les différentes étapes du parcours utilisateur,
* intégration et gestion des appels API INSEE,
* synchronisation avec Google Calendar,
* prévention des doublons en base de données,
* structuration des données du questionnaire dynamique,
* gestion de la logique métier liée aux certifications.

Ces défis m’ont permis de mieux comprendre l’organisation d’un backend Django et la conception d’applications plus complexes.

---

## Technologies utilisées

* Python
* Django
* SQLite / PostgreSQL
* HTML / CSS / JavaScript
* Google Calendar API
* API INSEE

---

## Pistes d’évolution

Voici quelques améliorations prévues pour les prochaines versions :

* ajout d’un dashboard administrateur,
* authentification utilisateur,
* API REST avec Django REST Framework,
* refonte frontend avec React ou Vue.js,
* génération automatique de devis,
* système avancé de suivi des dossiers,
* notifications et rappels automatiques.

---

# Installation du projet

## 1. Cloner le repository

```bash
git clone https://github.com/marissalmr/gbs_stage.git
cd gbs_stage
```

---

## 2. Créer un environnement virtuel

```bash
python -m venv env
```

### Activer l’environnement virtuel

#### Sur macOS / Linux

```bash
source env/bin/activate
```

#### Sur Windows

```bash
env\Scripts\activate
```

---

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 4. Appliquer les migrations

```bash
python manage.py migrate
```

---

## 5. Lancer le serveur

```bash
python manage.py runserver
```

---

## Accès à l’application

Une fois le serveur lancé :

```bash
http://127.0.0.1:8000/
```



