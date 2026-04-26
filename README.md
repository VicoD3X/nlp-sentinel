# Air Paradis Sentiment Monitor — NLP & MLOps Feedback Loop

[![CI](https://github.com/VicoD3X/nlp-sentinel/actions/workflows/ci.yml/badge.svg)](https://github.com/VicoD3X/nlp-sentinel/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-TF--IDF-F7931E?logo=scikitlearn&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-demo-FF4B4B?logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-MVP-0F172A)

## Présentation du projet

Air Paradis Sentiment Monitor est un MVP NLP/MLOps de classification de sentiment sur des tweets liés à une compagnie aérienne. Le dépôt relie un modèle baseline TF-IDF, une API FastAPI, une interface Streamlit, Azure App Insights et une boucle de feedback utilisateur pour signaler les mauvaises prédictions.

Le projet ne prétend pas être un système NLP industriel. Il montre une chaîne complète et compréhensible : expérimentation, artefact modèle, inférence API, démonstration utilisateur, monitoring et feedback.

## Objectif métier

L'objectif est d'aider une équipe produit à détecter rapidement si un tweet exprime un sentiment positif ou négatif, puis à collecter des signaux de correction lorsque l'utilisateur juge la prédiction incorrecte.

## Architecture générale

```text
.
|-- api/                    # API FastAPI officielle
|-- app/                    # Interface Streamlit
|-- src/sentiment_monitor/  # Configuration, inférence, monitoring et schémas
|-- models/                 # Artefact modèle léger utilisé en local
|-- notebooks/              # Exploration et modélisation NLP
|-- data/                   # Documentation des données attendues
|-- docs/                   # Documentation projet, monitoring, modèle et déploiement
|-- tests/                  # Tests unitaires légers
|-- requirements-api.txt
|-- requirements-app.txt
|-- requirements-dev.txt
`-- README.md
```

## Pipeline NLP

Le pipeline exploite le dataset Sentiment140 dans un notebook d'exploration. Le dépôt ne versionne pas le dataset complet. L'application finale utilise un artefact modèle déjà entraîné, stocké dans `models/tfidf_vectorizer.pkl`.

## Modèle utilisé

Le modèle est une baseline volontairement légère :

- vectorisation TF-IDF ;
- classification scikit-learn ;
- sortie binaire : `Négatif` ou `Positif` ;
- probabilité maximale exposée uniquement si le modèle la fournit.

Ce choix privilégie la lisibilité, la rapidité d'inférence et la simplicité de déploiement local.

## API FastAPI

L'API officielle est exposée par `api/main.py`.

```text
GET  /
POST /predict
```

Payload recommandé :

```json
{
  "texts": ["great flight", "horrible service"]
}
```

L'ancien format `["great flight", "horrible service"]` reste accepté pour compatibilité.

## Interface Streamlit

L'interface permet de :

- saisir un tweet ;
- lancer une prédiction ;
- afficher le sentiment détecté ;
- signaler une prédiction incorrecte.

Le parcours utilisateur reste volontairement simple afin de mettre en avant le flux NLP/MLOps plutôt qu'une interface produit complète.

## Monitoring Azure App Insights

Streamlit peut envoyer des événements vers Azure App Insights si `APPLICATIONINSIGHTS_CONNECTION_STRING` est configurée. Les logs contiennent le type d'événement, la prédiction, le label, la probabilité si disponible, la longueur du tweet et un aperçu tronqué du texte.

Le tweet brut complet n'est pas envoyé dans les dimensions de monitoring.

## Boucle de feedback utilisateur

Après une prédiction, l'utilisateur peut cliquer sur `Signaler comme incorrect`. Ce signalement est loggé comme événement distinct afin d'illustrer une boucle de feedback MLOps légère.

## Données et artefacts

- Le dataset complet Sentiment140 n'est pas versionné.
- Les données locales sont ignorées par Git.
- Le modèle léger `models/tfidf_vectorizer.pkl` est conservé pour permettre l'inférence locale.
- Les captures et documents historiques sont rangés dans `docs/`.

Voir aussi `data/README.md`, `models/README.md` et `docs/model-card.md`.

## Installation locale

Créer un environnement virtuel :

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Installer toutes les dépendances utiles au projet :

```bash
pip install -r requirements.txt
```

## Lancement de l'API

```bash
pip install -r requirements-api.txt
uvicorn api.main:app --reload
```

Documentation interactive :

```text
http://127.0.0.1:8000/docs
```

## Lancement de Streamlit

```bash
pip install -r requirements-app.txt
streamlit run app/streamlit_app.py
```

Azure App Insights est optionnel. Sans variable `APPLICATIONINSIGHTS_CONNECTION_STRING`, l'application fonctionne en local sans exporter de logs.

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

Les tests ne dépendent pas d'Azure et restent centrés sur l'inférence, le format API, le monitoring local et le nettoyage texte minimal.

## Notebook analytique

```bash
pip install -r requirements-dev.txt
jupyter lab
```

Le notebook principal est conservé dans `notebooks/01_sentiment_analysis_modeling.ipynb`.

## Limites actuelles

- Le modèle est une baseline TF-IDF, pas un modèle NLP avancé.
- Les scores ne sont pas présentés comme un benchmark scientifique complet.
- Le dataset complet n'est pas inclus.
- Le monitoring reste illustratif et dépend d'une configuration Azure externe.
- Le dépôt n'est pas une plateforme production-ready.

## Améliorations possibles

- Ajouter une évaluation plus structurée du modèle dans la documentation.
- Comparer plusieurs baselines légères sans alourdir l'application.
- Ajouter un export local des feedbacks utilisateurs.
- Définir une politique plus complète de réentraînement à partir des signalements.
- Préparer une démonstration cloud si le coût et la maintenance sont justifiés.

## Contexte du projet

Ce dépôt a été retravaillé comme projet portfolio NLP/MLOps. Il démontre la capacité à relier un modèle de machine learning, une API, une interface utilisateur, du monitoring et une boucle de feedback dans un MVP clair et maintenable.
