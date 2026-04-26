# Synthèse du projet

Air Paradis Sentiment Monitor est un MVP NLP/MLOps centré sur la classification de sentiment de tweets.

## Objectif

Le projet illustre une chaîne complète :

- exploration et modélisation NLP ;
- artefact modèle scikit-learn ;
- API FastAPI d'inférence ;
- interface Streamlit ;
- monitoring Azure App Insights ;
- feedback utilisateur sur les mauvaises prédictions.

## Positionnement

Le dépôt reste volontairement simple. Il ne cherche pas à devenir une plateforme NLP de production, mais à montrer une démarche claire, testable et compréhensible pour un portfolio Data Scientist / AI Engineer junior.

## Flux principal

1. L'utilisateur saisit un tweet dans Streamlit.
2. Le modèle prédit un sentiment positif ou négatif.
3. La prédiction peut être loggée dans Azure App Insights.
4. L'utilisateur peut signaler une prédiction incorrecte.
5. Ce signalement illustre une boucle de feedback MLOps légère.
