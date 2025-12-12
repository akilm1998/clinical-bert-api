from pydantic import BaseModel


class PredictIn(BaseModel):
    sentence: str


class PredictOut(BaseModel):
    label: str
    score: float
    time_ms: float
