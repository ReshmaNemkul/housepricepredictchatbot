from fastapi import APIRouter
from pydantic import BaseModel

from app.chatbot.parser import parse_message
from app.chatbot.response_generator import generate_response  # already handles preprocessing

router = APIRouter()

# ----------------------
# Mandatory Features
# ----------------------
MANDATORY_FEATURES = [
    "Bedroom",
    "Bathroom",
    "Floors",
    "Area_Aana",
    "Neighborhood_encoded"
]

# ----------------------
# User-friendly feature names
# ----------------------
FEATURE_FRIENDLY_NAMES = {
    "Bedroom": "Number of Bedrooms",
    "Bathroom": "Number of Bathrooms",
    "Floors": "Number of Floors",
    "Area_Aana": "Area (in Aana)",
    "Neighborhood_encoded": "Neighborhood"
}

# ----------------------
# Helper functions
# ----------------------
def check_missing_mandatory(entities: dict):
    """
    Returns a list of missing mandatory features.
    """
    missing = []
    for f in MANDATORY_FEATURES:
        if entities.get(f) is None or entities.get(f) == 0:
            missing.append(f)
    return missing

def format_missing_fields(missing_fields: list):
    """
    Converts feature keys to human-readable names.
    """
    friendly_list = [FEATURE_FRIENDLY_NAMES.get(f, f) for f in missing_fields]
    if len(friendly_list) > 1:
        return ", ".join(friendly_list[:-1]) + " and " + friendly_list[-1]
    elif friendly_list:
        return friendly_list[0]
    else:
        return ""

# ----------------------
# Request / Response Models
# ----------------------
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# ----------------------
# Chat Endpoint
# ----------------------
@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    user_message = request.message.strip()
    print("DEBUG: /chat endpoint received:", user_message)

    # Step 1: Parse message (intent + entities)
    parsed_data = parse_message(user_message)
    
    # Step 2: If it's a prediction request, check for missing mandatory fields
    if parsed_data["intent"] == "predict_price":
        missing_fields = check_missing_mandatory(parsed_data["entities"])
        if missing_fields:
            missing_str = format_missing_fields(missing_fields)
            return ChatResponse(
                response=f"To give you an accurate house price, I need a bit more information: {missing_str}. Could you provide that?"
            )

    # Step 3: Add original message for fallback FAQ matching
    parsed_data["original_message"] = user_message

    # Step 4: Generate response (either FAQ or price prediction)
    # ✅ The new response_generator now handles preprocessing internally
    reply = generate_response(parsed_data)

    # Step 5: Return proper response object
    return ChatResponse(response=reply)
