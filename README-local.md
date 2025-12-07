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