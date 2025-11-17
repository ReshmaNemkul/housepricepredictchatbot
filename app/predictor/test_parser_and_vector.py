import json
import sys
import os
import pprint
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.chatbot.parser import parse_message
from app.predictor.feature_extractor import build_feature_vector
# Example messages to test
test_messages = [
    "Price of a 2 bedroom 1 bathroom house in Kathmandu",
    "I want a 3 bedroom 2 bathroom house with gym and wifi in Imadol",
    "Looking for a 1500 sqft house"
]

for msg in test_messages:
    parsed = parse_message(msg)
    print("\nMessage:", msg)
    print("Parsed Entities:")
    pprint.pprint(parsed["entities"])
    
    vector = build_feature_vector(parsed["entities"])
    print("Feature Vector (length={}):".format(len(vector)))
    print(vector)
