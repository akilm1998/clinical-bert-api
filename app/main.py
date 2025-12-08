from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse

from app.model import get_pipeline
from app.schemas import PredictIn, PredictOut

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
    res = nlp(payload.sentence)[0]  # HuggingFace returns list
    return {"label": res["label"], "score": float(res["score"])}


@app.get("/health")
def health():
    if nlp is None:
        return JSONResponse(status_code=503, content={"status": "model not ready"})
    return {"status": "ok"}
