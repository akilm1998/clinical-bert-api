from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse

from app.model import get_pipeline
from app.schemas import PredictIn, PredictOut
import time

nlp = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global nlp
    # Load model once at startup
    nlp = get_pipeline()
    yield
    # On shutdown (optional cleanup)


app = FastAPI(
    lifespan=lifespan,
    title="Clinical BERT API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


@app.post("/predict", response_model=PredictOut)
def predict(payload: PredictIn):
    text = payload.sentence.strip()

    t_start = time.time()

    # Rule-based override for conditional sentences
    if text.lower().startswith("if"):
        # Run model once to get score (optional)
        model_out = nlp(text)[0]
        latency_ms = (time.time() - t_start) * 1000
        return {
            "label": "CONDITIONAL",
            "score": float(model_out["score"]),
            "time_ms": round(latency_ms, 2),
        }
    res = nlp(payload.sentence)[0]  # HuggingFace returns list
    latency_ms = (time.time() - t_start) * 1000
    return {
        "label": res["label"],
        "score": float(res["score"]),
        "time_ms": round(latency_ms, 2),
    }


@app.get("/health")
def health():
    if nlp is None:
        return JSONResponse(status_code=503, content={"status": "model not ready"})
    return {"status": "ok"}
