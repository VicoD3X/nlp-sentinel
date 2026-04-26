# Modèle

Le fichier `tfidf_vectorizer.pkl` est l'artefact léger utilisé par l'API FastAPI et l'interface Streamlit.

## Rôle

Il contient un pipeline scikit-learn de classification de sentiment basé sur :

- vectorisation TF-IDF ;
- classifieur supervisé ;
- prédiction binaire positive ou négative.

## Usage local

Le modèle est chargé par défaut depuis :

```text
models/tfidf_vectorizer.pkl
```

Le chemin peut être surchargé avec la variable d'environnement `MODEL_PATH`.

## Versionnement

Les modèles lourds ne doivent pas être multipliés dans Git. Seul cet artefact léger est conservé pour rendre la démo locale directement testable.
