# Données

Le dataset complet Sentiment140 n'est pas versionné dans ce dépôt.

## Source attendue

Les données originales suivent la structure Sentiment140. Selon la version utilisée, les colonnes brutes peuvent inclure :

- `target`
- `id`
- `date`
- `flag`
- `user`
- `text`

Le script de modélisation local attend au minimum un fichier préparé avec les colonnes :

- `target`
- `text`

## Convention locale

Les fichiers de données locaux sont ignorés par Git. Le notebook s'appuie sur un échantillon équilibré de 16 000 tweets pour garder une expérimentation exploitable localement.

Le fichier attendu par le script d'entraînement historique est :

```text
data/sentiment140_light.csv
```

## Versionnement

Ne versionner les données traitées que si elles sont petites, non sensibles et utiles à la compréhension du projet. Les exports volumineux ou intermédiaires doivent rester locaux.
