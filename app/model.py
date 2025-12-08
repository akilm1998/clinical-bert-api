from transformers import pipeline
from functools import lru_cache #least_recently_used

@lru_cache()
def get_pipeline():
    return pipeline("text-classification",
                    model="bvanaken/clinical-assertion-negation-bert",
                    truncation=True
                    )