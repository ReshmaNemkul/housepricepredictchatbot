from app.chatbot.faq_engine import match_faq
from app.predictor.model_utils import predict_price
from app.predictor.feature_extractor import preprocess_entities, build_feature_vector
from typing import Dict


def split_entities_for_model_and_chatbot(parsed_entities: dict):
    """
    Splits parsed entities into model-related features and chatbot-only data.
    """
    model_feature_keys = set([
        "Bedroom", "Bathroom", "Floors", "Area_Aana",
        "Neighborhood_encoded", "City_encoded", "Face_encoded", "Road Type_encoded",
        "Has_Air_condition", "Has_Backyard", "Has_Balcony", "Has_Cafeteria", "Has_Cctv",
        "Has_Deck", "Has_Drainage", "Has_Electricity_backup", "Has_Fencing", "Has_Frontyard",
        "Has_Garage", "Has_Garden", "Has_Gym", "Has_Intercom", "Has_Internet",
        "Has_Jacuzzi", "Has_Kids_playground", "Has_Lawn", "Has_Lift", "Has_Maintenance",
        "Has_Microwave", "Has_Modular_kitchen", "Has_Parking", "Has_Security_staff",
        "Has_Solar_water", "Has_Store_room", "Has_Swimming_pool", "Has_Tv_cable",
        "Has_Washing_machine", "Has_Water_supply", "Has_Water_tank", "Has_Water_well",
        "Has_Wifi"
    ])

    model_features = {}
    chatbot_text_data = {}

    for k, v in parsed_entities.items():
        if k in model_feature_keys:
            model_features[k] = v if v is not None else 0
        else:
            chatbot_text_data[k] = v

    return model_features, chatbot_text_data


def generate_response(parsed_data: Dict) -> str:
    """
    Generates a chatbot response based on intent:
    - FAQ
    - Price prediction
    """
    print("DEBUG: generate_response called with intent:", parsed_data.get("intent"))
    intent = parsed_data.get("intent")
    original_message = parsed_data.get("original_message", "")

    if intent == "faq":
        answer = match_faq(original_message)
        return answer if answer else "Sorry, I don't have an answer for that."

    elif intent == "predict_price":
        entities = parsed_data.get("entities", {})

        try:
            # ✅ Preprocess all categorical features first
            entities = preprocess_entities(entities)

            # ✅ Split entities into model features & chatbot text
            model_features, chatbot_text_data = split_entities_for_model_and_chatbot(entities)

            # Optional debug: check numeric conversion
            print("DEBUG: model_features after preprocessing:", model_features)

            # ✅ Build feature vector
            feature_vector = build_feature_vector(model_features)
            print("DEBUG: feature_vector length:", len(feature_vector))  # should match FEATURE_COLUMNS

            # ✅ Predict price
            price = predict_price(feature_vector)

            # Prepare response text
            neighborhood = chatbot_text_data.get("Neighborhood", "the specified area")
            bedrooms = model_features.get("Bedroom", 0)
            bathrooms = model_features.get("Bathroom", 0)

            bedrooms_text = f"{bedrooms}-bedroom" if bedrooms > 0 else "house"
            bathrooms_text = f", {bathrooms}-bathroom" if bathrooms > 0 else ""

            return (f"The estimated price for a {bedrooms_text}{bathrooms_text} "
                    f"house in {neighborhood} is NPR {round(price):,}")

        except Exception as e:
            return f"Prediction failed: {str(e)}"

    else:
        return "Sorry, I didn't understand that. Can you please rephrase?"
