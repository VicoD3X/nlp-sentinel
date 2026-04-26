from fastapi.testclient import TestClient

from api.main import app


def test_root_ok():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "Air Paradis Sentiment Monitor API" in response.json()["message"]


def test_predict_official_payload_ok():
    client = TestClient(app)
    response = client.post(
        "/predict",
        json={"texts": ["great flight", "horrible service"]},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["predictions"] in ([1, 0], [0, 1], [1, 1], [0, 0])
    assert len(payload["results"]) == 2
    assert {"text_index", "class_id", "label", "probability"} <= set(
        payload["results"][0],
    )


def test_predict_legacy_payload_ok():
    client = TestClient(app)
    response = client.post("/predict", json=["great flight", "horrible service"])

    assert response.status_code == 200
    assert len(response.json()["predictions"]) == 2
