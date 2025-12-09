# app/model.py
import logging
from functools import lru_cache
from transformers import pipeline
from transformers.pipelines import Pipeline

logger = logging.getLogger(__name__)


@lru_cache()
def get_pipeline(device: int = -1) -> Pipeline:  # Uses default cpu

    try:
        logger.info(
            "Loading HF pipeline: bvanaken/clinical-assertion-negation-bert (device=%s)",
            device,
        )
        p = pipeline(
            "text-classification",
            model="bvanaken/clinical-assertion-negation-bert",
            truncation=True,
            device=device,
        )
        logger.info("Pipeline loaded successfully")
        return p
    except Exception as e:
        logger.exception(f"Failed to load HF pipeline, {e}")
        raise
