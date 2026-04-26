from src.sentiment_monitor.inference import predict_batch, predict_sentiment


class FakeModel:
    def predict(self, texts):
        return [1 if "great" in texts[0].lower() else 0]

    def predict_proba(self, texts):
        if "great" in texts[0].lower():
            return [[0.1, 0.9]]
        return [[0.8, 0.2]]


def test_predict_sentiment_with_mock_model():
    result = predict_sentiment("great flight", model=FakeModel())

    assert result["class_id"] == 1
    assert result["label"] == "Positif"
    assert result["probability"] == 0.9


def test_predict_batch_adds_text_index():
    results = predict_batch(["great flight", "bad delay"], model=FakeModel())

    assert [result["text_index"] for result in results] == [0, 1]
    assert [result["label"] for result in results] == ["Positif", "Négatif"]


def test_predict_sentiment_rejects_empty_text():
    try:
        predict_sentiment("   ", model=FakeModel())
    except ValueError as exc:
        assert "vide" in str(exc)
    else:
        raise AssertionError("Une prédiction vide doit lever une ValueError.")
