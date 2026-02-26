import requests

API_KEY = "4eETqmiToAeqwMOVGI5i7CtrFSluArKXp1SUOjWf"

def get_calories(food_name):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "api_key": API_KEY,
        "query": food_name,
        "pageSize": 1
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        # Check if food found
        if "foods" not in data or len(data["foods"]) == 0:
            return "Not Available"

        food = data["foods"][0]

        for nutrient in food["foodNutrients"]:
            if nutrient["nutrientName"] == "Energy":
                return nutrient["value"]  # kcal

        return "Not Available"

    except Exception as e:
        print("Error:", e)
        return "Not Available"