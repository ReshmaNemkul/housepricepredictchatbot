# test_chatbot_prediction.py
from app.chatbot.response_generator import generate_response

# List of test cases
test_cases = [
    {
        "intent": "predict_price",
        "original_message": "3-bedroom house in Baneshwor",
        "entities": {
            "Bedroom": 3,
            "Bathroom": 2,
            "Floors": 2,
            "Area_Aana": 8,
            "Neighborhood_encoded": "Baneshwor",
            "Road Type_encoded": "Asphalt",
            "Face_encoded": "East",
            "City_encoded": "Kathmandu",
            "Has_Air_condition": 1,
            "Has_Backyard": 0,
            "Has_Balcony": 1
        }
    },
    {
        "intent": "predict_price",
        "original_message": "2-bedroom house in Lazimpat",
        "entities": {
            "Bedroom": 2,
            "Bathroom": 1,
            "Floors": 1,
            "Area_Aana": 5,
            "Neighborhood_encoded": "Lazimpat",
            "Road Type_encoded": "Gravel",
            "Face_encoded": "West",
            "City_encoded": "Kathmandu",
            "Has_Air_condition": 0,
            "Has_Backyard": 1,
            "Has_Balcony": 0
        }
    },
    {
        "intent": "predict_price",
        "original_message": "4-bedroom house in Thapathali",
        "entities": {
            "Bedroom": 4,
            "Bathroom": 3,
            "Floors": 2,
            "Area_Aana": 12,
            "Neighborhood_encoded": "Thapathali",
            "Road Type_encoded": "Asphalt",
            "Face_encoded": "South",
            "City_encoded": "Kathmandu",
            "Has_Air_condition": 1,
            "Has_Backyard": 1,
            "Has_Balcony": 1
        }
    }
]

# Run all test cases
for i, parsed_data in enumerate(test_cases, start=1):
    response = generate_response(parsed_data)
    print(f"Test Case {i}: {response}")
