import sys
import os
import json
import spacy
from typing import Optional
from app.core.config import DATA_DIR

# Load spaCy model
nlp = spacy.load("en_core_web_md")

# Load FAQs from JSON
faq_path = os.path.join(DATA_DIR, "faq_data.json")
with open(faq_path, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Build (question, answer) pairs
faq_pairs = []
for category in raw_data.values():
    questions = category.get("questions", [])
    answer = category.get("answer", "")
    for question in questions:
        faq_pairs.append((question, answer))

def match_faq(user_message: str, threshold: float = 0.75) -> Optional[str]:
    """
    Match user message to the most semantically similar FAQ question.
    Returns the answer if similarity is above threshold, else None.
    """
    user_doc = nlp(user_message.lower())
    best_score = 0
    best_answer = None

    for question, answer in faq_pairs:
        faq_doc = nlp(question.lower())
        score = user_doc.similarity(faq_doc)

        if score > best_score and score >= threshold:
            best_score = score
            best_answer = answer

    return best_answer

# Command line testing
if __name__ == "__main__":
    while True:
        user_input = input("Ask me a FAQ: ")
        answer = match_faq(user_input)
        print("Answer:", answer or "No good match found.")
