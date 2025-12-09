# import pytest
# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)

# @pytest.mark.parametrize("sentence,expected_label", [
#     ("The patient denies chest pain.", "ABSENT"),
#     ("He has a history of hypertension.", "PRESENT"),
#     ("If the patient experiences dizziness, reduce the dosage.", "CONDITIONAL"),
#     ("No signs of pneumonia were observed.", "ABSENT"),
# ])
# def test_predict_labels_and_meta(sentence, expected_label):
#     """
#     Integration-style test hitting the real pipeline from app.main.
#     This will load the HF model at startup (can be slow on first run).
#     """
#     response = client.post("/predict", json={"sentence": sentence})
#     assert response.status_code == 200, f"unexpected status: {response.status_code} / {response.text}"

#     data = response.json()

#     # Basic shape & correctness checks
#     assert "label" in data and "score" in data and "time_ms" in data, f"missing keys in response: {data.keys()}"
#     assert data["label"] == expected_label, f"label mismatch for `{sentence}`: got {data['label']} expected {expected_label}"

#     # check score 
#     assert isinstance(data["score"], float), "score should be float"
#     assert 0.0 <= data["score"] <= 1.0, f"score out of range: {data['score']}"

#     # Check latnecy
#     assert isinstance(data["time_ms"], (float, int)), "time_ms should be numeric"
#     assert data["time_ms"] >= 0, f"time_ms negative: {data['time_ms']}"


# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

TEST_CASES = [
    ("The patient denies chest pain.", "ABSENT"),
    ("He has a history of hypertension.", "PRESENT"),
    ("If the patient experiences dizziness, reduce the dosage.", "CONDITIONAL"),
    ("No signs of pneumonia were observed.", "ABSENT"),
]

@pytest.mark.parametrize("sentence,expected_label", TEST_CASES)
def test_predict_labels_and_meta(sentence, expected_label):
    """
    Use TestClient as context manager so startup (lifespan) runs fully and
    any startup exceptions are raised here, giving clear test failure messages.
    """
    with TestClient(app) as client:
        response = client.post("/predict", json={"sentence": sentence})
        assert response.status_code == 200, f"unexpected status: {response.status_code} / {response.text}"

        data = response.json()
        assert "label" in data and "score" in data and "time_ms" in data
        assert data["label"] == expected_label, f"label mismatch for `{sentence}`: got {data['label']} expected {expected_label}"
        assert isinstance(data["score"], float)
        assert 0.0 <= data["score"] <= 1.0
        assert isinstance(data["time_ms"], (float, int)) and data["time_ms"] >= 0
