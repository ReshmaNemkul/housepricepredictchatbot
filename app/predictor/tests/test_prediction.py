# app/predictor/tests/test_prediction.py

from app.predictor.feature_extractor import build_feature_vector
from app.predictor.model_utils import predict_price

# Simulate parsed message output from NLP
parsed_entities = {
    "Bedroom": 3,
    "Bathroom": 2,
    "Floors": 2,
    "Neighborhood_encoded": 64,
    "Has_Air_condition": 1,
    "Has_Backyard": 1,
    "Has_Balcony": 1,
    "Has_Cafeteria": 0,
    "Has_Cctv": 0,
    "Has_Deck": 0,
    "Has_Drainage": 1,
    "Has_Electricity_backup": 1,
    "Has_Fencing": 1,
    "Has_Frontyard": 1,
    "Has_Garage": 0,
    "Has_Garden": 1,
    "Has_Gym": 0,
    "Has_Intercom": 0,
    "Has_Internet": 1,
    "Has_Jacuzzi": 0,
    "Has_Kids_playground": 0,
    "Has_Lawn": 1,
    "Has_Lift": 1,
    "Has_Maintenance": 0,
    "Has_Microwave": 0,
    "Has_Modular_kitchen": 1,
    "Has_Parking": 1,
    "Has_Security_staff": 1,
    "Has_Solar_water": 0,
    "Has_Store_room": 0,
    "Has_Swimming_pool": 0,
    "Has_Tv_cable": 1,
    "Has_Washing_machine": 0,
    "Has_Water_supply": 1,
    "Has_Water_tank": 1,
    "Has_Water_well": 0,
    "Has_Wifi": 1,
    "Area_Aana": 14.5,
    "City_encoded": 9,
    "Face_encoded": 0,
    "Road Type_encoded": 1
}

# Add derived fields like Total_Rooms, Amenity_Count, Is_Luxury_House automatically
features = build_feature_vector(parsed_entities)

# Predict price
predicted_price = predict_price(features)

print(f"🏡 Predicted House Price: Rs. {predicted_price:.2f} lakhs")
