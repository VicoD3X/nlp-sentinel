# Model Card — TF-IDF Sentiment Baseline

## Type de modèle

Baseline NLP supervisée basée sur un pipeline scikit-learn :

- `TfidfVectorizer`
- classifieur binaire supervisé

## Dataset

Le projet s'appuie sur Sentiment140. Le dataset complet n'est pas versionné. Le notebook documente l'utilisation d'un échantillon équilibré de 16 000 tweets.

## Objectif prévu

Classifier un texte court de type tweet en sentiment :

- `Négatif`
- `Positif`

## Usage prévu

Le modèle sert à alimenter une API et une interface Streamlit de démonstration. Il est adapté à un MVP portfolio et à une lecture pédagogique du flux MLOps.

## Non-usage

Le modèle ne doit pas être présenté comme :

- un système NLP industriel ;
- un outil fiable pour modérer automatiquement des contenus ;
- une solution robuste à tous les contextes linguistiques ;
- une preuve de performance supérieure à des modèles modernes.

## Limites

- Baseline légère, dépendante de la qualité de l'échantillon.
- Sensibilité possible au vocabulaire, à l'ironie et au contexte.
- Pas d'analyse détaillée des biais dans cette version.
- Scores non détaillés dans la documentation principale afin de ne pas inventer de résultats.
