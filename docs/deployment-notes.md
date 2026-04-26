# Notes de déploiement

## Mode recommandé

Le mode recommandé pour évaluer le projet est le lancement local :

```bash
uvicorn api.main:app --reload
streamlit run app/streamlit_app.py
```

## Streamlit

Le `Procfile` actuel lance l'interface Streamlit :

```text
web: streamlit run app/streamlit_app.py --server.address=0.0.0.0 --server.port=$PORT
```

Il est conservé comme trace de déploiement simple.

## API

Un exemple de Procfile API est fourni dans `Procfile.api.example` :

```text
web: uvicorn api.main:app --host=0.0.0.0 --port=$PORT
```

## Azure App Insights

Le monitoring dépend de `APPLICATIONINSIGHTS_CONNECTION_STRING`. Il est optionnel pour le lancement local.

## Limite de promesse

Le dépôt ne promet pas un service cloud actif. L'objectif portfolio est de montrer l'architecture, le flux d'inférence, le monitoring et le feedback utilisateur.
