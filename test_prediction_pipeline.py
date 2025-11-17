# test_prediction_pipeline.py

from app.chatbot.response_generator import generate_response
from app.chatbot.response_generator import split_entities_for_model_and_chatbot
from app.predictor.feature_extractor import build_feature_vector
from app.predictor.model_utils import predict_price

# Example of parsed entities output from parser for a price prediction request
sample_parsed_entities = {
    "Bedroom": 3,
    "Bathroom": 2,
    "Floors": 2,
    "Area_Aana": 10,
    "Neighborhood_encoded": 5,
    "City_encoded": 2,
    "Face_encoded": 1,
    "Road Type_encoded": 3,
    "Has_Air_condition": 1,
    "Has_Backyard": 0,
    "Has_Balcony": 1,
    # Add other features with 0 or 1 as applicable...
}

# Also include the raw string entity for natural response
sample_chatbot_text_data = {
    "Neighborhood": "Imadol",
    "City": "Lalitpur",
}

# Construct parsed_data dictionary like parser output
parsed_data = {
    "intent": "predict_price",
    "entities": {**sample_parsed_entities, **sample_chatbot_text_data},
    "original_message": "What is the price for a 3 bedroom 2 bathroom house in Imadol?"
}

def test_pipeline(parsed_data):
    print("Testing prediction pipeline...")

    # Step 0: Split entities
    model_features, chatbot_text_data = split_entities_for_model_and_chatbot(parsed_data["entities"])

    print("Model features:", model_features)
    print("Chatbot text data:", chatbot_text_data)

    # Step 1: Build feature vector
    feature_vector = build_feature_vector(model_features)
    print("Feature vector length:", len(feature_vector))

    # Step 2: Predict price
    price = predict_price(feature_vector)
    print(f"Predicted price: NPR {round(price):,}")

    # Step 3: Generate response
    response = generate_response(parsed_data)
    print("Generated response:", response)

if __name__ == "__main__":
    test_pipeline(parsed_data)
