# import json
import os
import numpy as np
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load feature columns
FEATURE_PATH = os.path.join(BASE_DIR, "..", "data", "features.json")
with open(FEATURE_PATH, 'r') as f:
    FEATURE_COLUMNS = json.load(f)


# -----------------------------
# FIXED: Load categorical mappings correctly
# -----------------------------

# Neighborhood
NEIGHBORHOOD_PATH = os.path.join(BASE_DIR, "..", "data", "neighborhood_mapping.json")
with open(NEIGHBORHOOD_PATH, 'r') as f:
    NEIGHBORHOOD_MAP = json.load(f).get("Neighborhood", {})

# Road Type
ROADTYPE_PATH = os.path.join(BASE_DIR, "..", "data", "roadtype_mapping.json")
with open(ROADTYPE_PATH, 'r') as f:
    ROADTYPE_MAP = json.load(f).get("RoadType", {})

# Face
FACE_PATH = os.path.join(BASE_DIR, "..", "data", "face_mapping.json")
with open(FACE_PATH, 'r') as f:
    FACE_MAP = json.load(f).get("Face", {})

# City
CITY_PATH = os.path.join(BASE_DIR, "..", "data", "city_mapping.json")
with open(CITY_PATH, 'r') as f:
    CITY_MAP = json.load(f).get("City", {})


# -----------------------------
# Preprocess categorical entities
# -----------------------------
def preprocess_entities(entities: dict) -> dict:
    """Convert categorical strings into numeric codes before building feature vector."""

    if "Neighborhood_encoded" in entities and isinstance(entities["Neighborhood_encoded"], str):
        entities["Neighborhood_encoded"] = NEIGHBORHOOD_MAP.get(
            entities["Neighborhood_encoded"].strip(), 0
        )

    if "Road Type_encoded" in entities and isinstance(entities["Road Type_encoded"], str):
        entities["Road Type_encoded"] = ROADTYPE_MAP.get(
            entities["Road Type_encoded"].strip(), 0
        )

    if "Face_encoded" in entities and isinstance(entities["Face_encoded"], str):
        entities["Face_encoded"] = FACE_MAP.get(
            entities["Face_encoded"].strip(), 0
        )

    if "City_encoded" in entities and isinstance(entities["City_encoded"], str):
        entities["City_encoded"] = CITY_MAP.get(
            entities["City_encoded"].strip(), 0
        )

    return entities


# -----------------------------
# Build feature vector for model
# -----------------------------
def build_feature_vector(parsed_entities: dict) -> list:
    """Convert entities into ordered numeric vector for model."""
    entity_defaults = {col: 0 for col in FEATURE_COLUMNS}

    for key, value in parsed_entities.items():
        if key in entity_defaults and value is not None:
            try:
                val = float(value)
                if np.isfinite(val):
                    entity_defaults[key] = val
            except:
                entity_defaults[key] = 0

    return [entity_defaults[col] for col in FEATURE_COLUMNS]
