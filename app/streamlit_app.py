from __future__ import annotations

import streamlit as st

from src.sentiment_monitor.config import get_config
from src.sentiment_monitor.inference import load_model, predict_sentiment
from src.sentiment_monitor.monitoring import (
    get_monitoring_logger,
    log_bad_prediction,
    log_prediction,
)


CONFIG = get_config()


@st.cache_resource
def get_model(model_path: str):
    """Charge le modèle une seule fois par session Streamlit."""
    return load_model(model_path)


@st.cache_resource
def get_logger():
    """Configure le logger Azure App Insights si la variable est disponible."""
    return get_monitoring_logger(CONFIG)


st.set_page_config(
    page_title="Air Paradis Sentiment Monitor",
    layout="centered",
)

st.title("Air Paradis Sentiment Monitor")
st.caption("Démonstration NLP/MLOps : sentiment, monitoring et feedback utilisateur.")

st.markdown(
    """
Cette interface illustre un flux MVP volontairement simple :
saisir un tweet, prédire son sentiment, puis signaler une mauvaise prédiction.

Le modèle utilisé est une baseline TF-IDF / scikit-learn. Les logs de monitoring
ne stockent qu'un aperçu tronqué du texte afin de limiter l'exposition des données.
"""
)

try:
    model = get_model(str(CONFIG.model_path))
    logger = get_logger()
except Exception as exc:
    st.error(f"Impossible de charger la démonstration : {exc}")
    st.stop()

tweet = st.text_area(
    "Saisissez un tweet",
    height=120,
    placeholder="Exemple : Flight delayed again...",
)

if "last_tweet" not in st.session_state:
    st.session_state.last_tweet = None
if "last_pred" not in st.session_state:
    st.session_state.last_pred = None
if "last_label" not in st.session_state:
    st.session_state.last_label = None
if "last_proba" not in st.session_state:
    st.session_state.last_proba = None

col1, col2 = st.columns(2)

with col1:
    predict_clicked = st.button("Prédire", type="primary", key="btn_predict")

if predict_clicked:
    if not tweet.strip():
        st.warning("Veuillez saisir un tweet.")
    else:
        try:
            result = predict_sentiment(tweet, model=model)
        except Exception as exc:
            st.error(f"Erreur lors de la prédiction : {exc}")
        else:
            pred = int(result["class_id"])
            label = str(result["label"])
            proba = result["probability"]

            st.success(f"Sentiment détecté : {label}")

            st.session_state.last_tweet = tweet
            st.session_state.last_pred = pred
            st.session_state.last_label = label
            st.session_state.last_proba = proba

            try:
                log_prediction(tweet, pred, label, proba, logger=logger)
            except Exception as exc:
                st.warning(f"Échec du log Azure App Insights : {exc}")

with col2:
    if st.session_state.last_pred is not None:
        if st.button("Signaler comme incorrect", key="btn_feedback"):
            try:
                log_bad_prediction(
                    st.session_state.last_tweet,
                    st.session_state.last_pred,
                    st.session_state.last_label,
                    st.session_state.last_proba,
                    logger=logger,
                )
                st.success("Merci, votre signalement a été enregistré.")
            except Exception as exc:
                st.error(f"Impossible d'envoyer le signalement : {exc}")
