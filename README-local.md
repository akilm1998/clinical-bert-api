# Local Development & Model Testing

This document contains the steps to set up the local environment and test the
Clinical Assertion Negation BERT model before integrating it into the API layer.

## 1. Requirements
- Python >= 3.10

## 2. Create and activate a virtual environment

### macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
```
### Windows
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

## 3. Install local dependencies
These dependencies are only for local model testing and development.
```bash
pip install -r requirements-local.txt
```

## 4. Run a sample inference
You can test the model using the standalone script local_run.py
```bash
python local_run.py --text "text for inference / testing"
```

### Example output
```bash
Device set to use cpu
[{'label': 'ABSENT', 'score': 0.8873447775840759}]
```

# 5. Running the FastAPI Application

Start the API using Uvicorn:

```bash
uvicorn app.main:app --reload
```

### Endpoints:
| Endpoint | Description |
|---------|-------------|
| `/predict` | Real-time inference endpoint |
| `/health` | Model readiness & health check |

FastAPI's automatic docs:
```
http://localhost:8000/docs
```

---

# 6. Predict Endpoint Usage

### Example:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sentence": "The patient denies chest pain."}'
```
#### Windows
```bash
Invoke-WebRequest `
  -Uri http://127.0.0.1:8000/predict `
  -Method POST `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"sentence":"The patient denies chest pain."}'`
```

### Example response:
```json
{
  "label": "ABSENT",
  "score": 0.98,
  "time_ms": 42.1
}
```

---

# 7. Health Check
## Linux
```bash
curl http://localhost:8000/health
```
## Windows
```bash
Invoke-RestMethod `
  -Uri http://localhost:8000/health `
  -Method GET `
```
Returns:
```json
{"status": "ok"}
```

If the model has not initialized:
```json
{"status": "model not ready"}
```

---