# import spacy
# import re
# import json
# import os

# nlp = spacy.load("en_core_web_md")

# # --- Helper to load and lowercase mapping dicts ---
# def load_mapping(json_path: str, key: str) -> dict:
#     with open(json_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)
#     return {k.lower(): v for k, v in data.get(key, {}).items()}

# # --- Paths ---
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# data_dir = os.path.join(BASE_DIR, 'data')

# NEIGHBORHOOD_MAP = load_mapping(os.path.join(data_dir, 'neighborhood_mapping.json'), "Neighborhood")
# CITY_MAP = load_mapping(os.path.join(data_dir, 'city_mapping.json'), "City")
# FACE_MAP = load_mapping(os.path.join(data_dir, 'face_mapping.json'), "Face")
# ROADTYPE_MAP = load_mapping(os.path.join(data_dir, 'roadtype_mapping.json'), "RoadType")

# # --- Area Unit Conversion Helper ---
# def convert_to_aana(number: float, unit: str) -> float:
#     unit = unit.lower()
#     conversion_factors = {
#         "aana": 1, "ana": 1,
#         "ropani": 16,
#         "paisa": 0.25,
#         "dam": 0.0625,
#         "sqft": 1 / 342.25,
#         "square feet": 1 / 342.25,
#         "sqm": 10.7639 / 342.25,
#         "square meter": 10.7639 / 342.25,
#         "square meters": 10.7639 / 342.25,
#     }
#     return round(number * conversion_factors.get(unit, 0), 2)

# # --- Main Parser Function ---
# def parse_message(text: str) -> dict:
#     text_lower = text.lower()
#     doc = nlp(text_lower)

#     # --- Intent detection ---
#     intent = "predict_price" if re.search(r"\b(price|cost|rent|value|how much)\b", text_lower) else "faq"

#     def extract_numeric_feature(keywords):
#         for token in doc:
#             if token.like_num:
#                 window = doc[max(0, token.i - 3): token.i + 4]
#                 if any(w.text.lower() in keywords for w in window):
#                     try:
#                         return int(token.text)
#                     except:
#                         return None
#         return None

#     bedrooms = extract_numeric_feature(["bed", "bedroom", "bedrooms","room","rooms"])
#     bathrooms = extract_numeric_feature(["bath", "bathroom", "bathrooms", "toilet","washroom"])
#     floors = extract_numeric_feature(["floor", "floors", "storey", "story", "level", "talla"])

#     # --- Area extraction and conversion ---
#     area_aana = None
#     area_units = [
#         "aana", "ana", "ropani", "paisa", "dam",
#         "sqft", "square feet", "sqm", "square meter", "square meters"
#     ]
#     for i, token in enumerate(doc):
#         if token.like_num:
#             window = doc[i:i+4]
#             window_text = " ".join([t.text.lower() for t in window])
#             for unit in area_units:
#                 if unit in window_text:
#                     try:
#                         area_aana = convert_to_aana(float(token.text), unit)
#                         break
#                     except:
#                         pass
#         if area_aana is not None:
#             break

#     def match_from_map(mapping):
#         for key in mapping:
#             if re.search(rf"\b{re.escape(key)}\b", text_lower):
#                 return key, mapping[key]
#         return None, None

#     neighborhood, neighborhood_encoded = match_from_map(NEIGHBORHOOD_MAP)
#     city, city_encoded = match_from_map(CITY_MAP)
#     face, face_encoded = match_from_map(FACE_MAP)
#     road_type, road_type_encoded = match_from_map(ROADTYPE_MAP)

#     # --- Final structured output ---
#     return {
#         "intent": intent,
#         "entities": {
#             "Bedroom": bedrooms,
#             "Bathroom": bathrooms,
#             "Area_Aana": area_aana,
#             "Floors": floors,
#             "neighborhood": neighborhood,
#             "neighborhood_encoded": neighborhood_encoded,
#             "city": city,
#             "city_encoded": city_encoded,
#             "face": face,
#             "face_encoded": face_encoded,
#             "road_type": road_type,
#             "road_type_encoded": road_type_encoded   
#         }
#     }

# # --- Quick test if run directly ---
# if __name__ == "__main__":
#     test_messages = [
#         "How much is a 3 bedroom 2 bathroom house in Imadol with 1200 square feet and 2 floors facing east?",
#         "Looking for a 1500 sqft house with blacktop road and north facing.",
#         "Price for 10 aana house with 3 bedrooms?",
#         "I want a 3 bedroom house in Imadol, Kathmandu with 1200 sqft.",
#         "What’s the refund policy?",
#     ]
#     for msg in test_messages:
#         print("\nInput:", msg)
#         print("Parsed:", parse_message(msg))
import spacy
import re
import json
import os

nlp = spacy.load("en_core_web_md")

# --- Helper to load and lowercase mapping dicts ---
def load_mapping(json_path: str, key: str) -> dict:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return {k.lower(): v for k, v in data.get(key, {}).items()}

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(BASE_DIR, 'data')

NEIGHBORHOOD_MAP = load_mapping(os.path.join(data_dir, 'neighborhood_mapping.json'), "Neighborhood")
CITY_MAP = load_mapping(os.path.join(data_dir, 'city_mapping.json'), "City")
FACE_MAP = load_mapping(os.path.join(data_dir, 'face_mapping.json'), "Face")
ROADTYPE_MAP = load_mapping(os.path.join(data_dir, 'roadtype_mapping.json'), "RoadType")

# --- Area Unit Conversion Helper ---
def convert_to_aana(number: float, unit: str) -> float:
    unit = unit.lower()
    conversion_factors = {
        "aana": 1, "ana": 1,
        "ropani": 16,
        "paisa": 0.25,
        "dam": 0.0625,
        "sqft": 1 / 342.25,
        "square feet": 1 / 342.25,
        "sqm": 10.7639 / 342.25,
        "square meter": 10.7639 / 342.25,
        "square meters": 10.7639 / 342.25,
    }
    return round(number * conversion_factors.get(unit, 0), 2)

# --- Entity Synonyms ---
ENTITY_SYNONYMS = {
    "Bedroom": ["bed", "bedroom", "bedrooms", "room", "rooms"],
    "Bathroom": ["bath", "bathroom", "bathrooms", "toilet", "washroom"],
    "Floors": ["floor", "floors", "storey", "story", "level", "talla"]
}

# --- Detect intent first ---
def detect_intent(text: str) -> str:
    text_lower = text.lower()
    price_keywords = r"\b(price|cost|rent|value|how much)\b"
    house_keywords = r"\b(bed|bedroom|room|floors?|storey|story|aana|sqft|square|ropani|bath|bathroom)\b"

    if re.search(price_keywords, text_lower):
        return "predict_price"
    elif re.search(house_keywords, text_lower):
        return "predict_price"
    return "faq"

# --- Normalize entity keys ---
def normalize_entities(entities: dict) -> dict:
    normalized = {}
    for key, synonyms in ENTITY_SYNONYMS.items():
        for syn in synonyms:
            if entities.get(syn) is not None:
                normalized[key] = entities[syn]
                break
        if key not in normalized:
            normalized[key] = entities.get(key, None)
    # Keep remaining keys
    for k in entities:
        if k not in normalized:
            normalized[k] = entities[k]
    return normalized

# --- Extract numeric feature helper ---
def extract_numeric_feature(doc, keywords):
    for token in doc:
        if token.like_num:
            window = doc[max(0, token.i - 3): token.i + 4]
            if any(w.text.lower() in keywords for w in window):
                try:
                    return int(token.text)
                except:
                    return None
    return None

# --- Extract map-based entity ---
def match_from_map(text_lower, mapping):
    for key in mapping:
        if re.search(rf"\b{re.escape(key)}\b", text_lower):
            return key, mapping[key]
    return None, None

# --- Main Parser Function ---
def parse_message(text: str) -> dict:
    text_lower = text.lower()
    doc = nlp(text_lower)

    # Step 1: Detect intent
    intent = detect_intent(text)

    if intent == "faq":
        # For FAQs, no need to extract heavy features
        return {"intent": "faq", "entities": {}}

    # Step 2: Extract entities (only if intent = predict_price)
    raw_entities = {
        "Bedroom": extract_numeric_feature(doc, ENTITY_SYNONYMS["Bedroom"]),
        "Bathroom": extract_numeric_feature(doc, ENTITY_SYNONYMS["Bathroom"]),
        "Floors": extract_numeric_feature(doc, ENTITY_SYNONYMS["Floors"]),
        "Area_Aana": None
    }

    # --- Area extraction ---
    area_units = ["aana", "ana", "ropani", "paisa", "dam", "sqft", "square feet", "sqm", "square meter", "square meters"]
    area_aana = None
    for i, token in enumerate(doc):
        if token.like_num:
            window = doc[i:i+4]
            window_text = " ".join([t.text.lower() for t in window])
            for unit in area_units:
                if unit in window_text:
                    try:
                        area_aana = convert_to_aana(float(token.text), unit)
                        break
                    except:
                        pass
        if area_aana is not None:
            break
    raw_entities["Area_Aana"] = area_aana

    # --- Map-based entities ---
    neighborhood, neighborhood_encoded = match_from_map(text_lower, NEIGHBORHOOD_MAP)
    city, city_encoded = match_from_map(text_lower, CITY_MAP)
    face, face_encoded = match_from_map(text_lower, FACE_MAP)
    road_type, road_type_encoded = match_from_map(text_lower, ROADTYPE_MAP)

    raw_entities.update({
        "neighborhood": neighborhood,
        "neighborhood_encoded": neighborhood_encoded,
        "city": city,
        "city_encoded": city_encoded,
        "face": face,
        "face_encoded": face_encoded,
        "road_type": road_type,
        "road_type_encoded": road_type_encoded
    })

    # Step 3: Normalize synonyms
    normalized_entities = normalize_entities(raw_entities)

    return {
        "intent": intent,
        "entities": normalized_entities
    }

# --- Quick test if run directly ---
if __name__ == "__main__":
    test_messages = [
        "How much is a 3 bedroom 2 bathroom house in Imadol with 1200 square feet and 2 floors facing east?",
        "Looking for a 1500 sqft house with blacktop road and north facing.",
        "Price for 10 aana house with 3 bedrooms?",
        "I want a 3 room house in Imadol, Kathmandu with 1200 sqft.",
        "What’s the refund policy?",
    ]
    for msg in test_messages:
        print("\nInput:", msg)
        print("Parsed:", parse_message(msg))
