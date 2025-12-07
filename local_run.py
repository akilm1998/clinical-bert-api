import argparse
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline

DEFAULT_TEXT = "The patient recovered during the night and now denies any shortness of breath."

parser = argparse.ArgumentParser()
parser.add_argument('--text', metavar='text', type=str, default=DEFAULT_TEXT)
args = parser.parse_args()

text = args.text

tokenizer = AutoTokenizer.from_pretrained("bvanaken/clinical-assertion-negation-bert")
model = AutoModelForSequenceClassification.from_pretrained("bvanaken/clinical-assertion-negation-bert")

# text = "The patient recovered during the night and now denies any [entity] shortness of breath [entity]."

classifier = TextClassificationPipeline(model=model, tokenizer=tokenizer)

classification = classifier(text)
print(classification)
# [{'label': 'ABSENT', 'score': 0.9842607378959656}]

