# import pickle

# with open("app/data/.pkl", "rb") as f:
#     model = pickle.load(f)

# print(type(model))
# import pickle

# with open("app/data/random_forest_model.pkl", "rb") as f:
#     obj = pickle.load(f)

# print(type(obj))
# import pickle

# files = [
#     "model_training/random_forest_model.pkl",
#     "model_training/random_forest_39features.pkl"
# ]

# for file in files:
#     with open(file, "rb") as f:
#         obj = pickle.load(f)
#     print(file, "->", type(obj))

import pickle

# Path to the model
model_path = "app/data/house_price_model_final.pkl"

# Load the model
with open(model_path, "rb") as f:
    model = pickle.load(f)

# Print the type of the loaded model
print(f"Loaded model from {model_path} ->", type(model))
