import os
import pandas as pd

# Get project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to nutrition.csv (inside data folder)
NUTRITION_PATH = os.path.join(BASE_DIR, "..", "data", "nutrition.csv")

# Load nutrition dataset
nutrition_df = pd.read_csv(NUTRITION_PATH)
def get_nutrition(food_name):

    if food_name is None:
        return None

    food_name = str(food_name).lower()

    food = nutrition_df[
        nutrition_df["food_name"].str.lower() == food_name
    ]

    if food.empty:
        return None

    return food.iloc[0]