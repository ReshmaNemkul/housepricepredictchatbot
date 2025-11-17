import os
import joblib
import pandas as pd
import numpy as np
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "data", "house_price_model_final.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "..", "data", "features.json")

# Load model
model = joblib.load(MODEL_PATH)

# Load feature names
with open(FEATURES_PATH, 'r') as f:
    FEATURE_COLUMNS = json.load(f)

def predict_price(feature_vector: list) -> float:
    X = pd.DataFrame([feature_vector], columns=FEATURE_COLUMNS)
    price = model.predict(X)[0]
    return float(price)
