from src.sentiment_monitor.inference import load_model


def test_model_file_loads_and_predicts():
    model = load_model("models/tfidf_vectorizer.pkl")
    predictions = model.predict(["I love this airline", "I hate delays"])

    assert len(predictions) == 2
    assert set(predictions).issubset({0, 1})
