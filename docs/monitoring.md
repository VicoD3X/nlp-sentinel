# Monitoring local et Azure App Insights

## Rôle

Le monitoring illustre une boucle MLOps légère : suivre les prédictions et les signalements utilisateur afin d'identifier les cas où le modèle peut être amélioré.

Le projet propose deux variantes :

- monitoring local maison, activé par défaut ;
- export Azure App Insights, conservé comme option si une connexion Azure est disponible.

## Événements

Deux types d'événements sont utilisés :

- `predict_api` : prédiction effectuée depuis Streamlit ou l'API ;
- `bad_pred` : prédiction signalée comme incorrecte par l'utilisateur.

## Variante locale

Par défaut, les événements sont écrits localement au format JSON Lines dans :

```text
logs/monitoring_events.jsonl
```

Chaque ligne contient :

- timestamp UTC ;
- niveau de log ;
- nom du logger ;
- type d'événement ;
- dimensions métier sécurisées.

Le chemin peut être modifié avec :

```text
LOCAL_MONITORING_PATH
```

Exemple :

```powershell
$env:LOCAL_MONITORING_PATH="logs/sentiment_monitoring.jsonl"
```

## Variante Azure

Azure App Insights reste disponible si le projet est lancé avec une connection string :

```text
APPLICATIONINSIGHTS_CONNECTION_STRING
```

Le backend se choisit avec :

```text
MONITORING_BACKEND
```

Valeurs disponibles :

- `local` : écrit uniquement dans le fichier local, valeur par défaut ;
- `azure` : envoie uniquement vers Azure App Insights ;
- `both` : écrit en local et envoie vers Azure ;
- `none` : désactive les handlers de monitoring.

## Données loggées

Les dimensions de log incluent :

- type d'événement ;
- source ;
- classe prédite ;
- label lisible ;
- probabilité si disponible ;
- longueur du tweet ;
- aperçu tronqué du tweet.

Le texte brut complet n'est pas envoyé. L'aperçu est limité par défaut à 160 caractères via `TWEET_PREVIEW_CHARS`.

## Limites confidentialité

Même tronqué, un tweet peut contenir des informations personnelles. Dans un contexte réel, il faudrait définir une politique plus stricte de minimisation, rétention et anonymisation.
