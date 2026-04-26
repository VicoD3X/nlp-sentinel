# Monitoring Azure App Insights

## Rôle

Le monitoring illustre une boucle MLOps légère : suivre les prédictions et les signalements utilisateur afin d'identifier les cas où le modèle peut être amélioré.

## Événements

Deux types d'événements sont utilisés :

- `predict_api` : prédiction effectuée depuis Streamlit ;
- `bad_pred` : prédiction signalée comme incorrecte par l'utilisateur.

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

## Configuration

Azure App Insights est activé uniquement si la variable suivante est définie :

```text
APPLICATIONINSIGHTS_CONNECTION_STRING
```

Sans cette variable, l'application fonctionne normalement en local sans export externe.

## Limites confidentialité

Même tronqué, un tweet peut contenir des informations personnelles. Dans un contexte réel, il faudrait définir une politique plus stricte de minimisation, rétention et anonymisation.
