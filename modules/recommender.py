def disease_filter(nutrition_data, diseases):
    warnings = []

    if "Diabetes" in diseases and nutrition_data["carbs"] > 30:
        warnings.append("High carbs not suitable for Diabetes")

    if "Hypertension" in diseases and nutrition_data["fat"] > 15:
        warnings.append("High fat not ideal for Hypertension")

    return warnings

def recommend_alternative(goal):
    if goal == "Weight Loss":
        return "Try grilled vegetables or salad"
    elif goal == "Weight Gain":
        return "Try high protein meals like paneer or chicken"
    else:
        return "Maintain balanced nutrition"
    
def meal_plan(goal):

    if goal == "Weight Gain":

        return """
### 🍳 Breakfast:
• Paneer stuffed paratha with ghee  
• Oats cooked in full-fat milk with nuts  
• Banana peanut butter smoothie  

### 🍛 Lunch:
• Chicken curry with rice and dal  
• Rajma chawal with curd  
• Paneer butter masala with roti  

### 🍲 Dinner:
• Mutton curry with chapati  
• Egg bhurji with butter toast  
• Vegetable pulao with curd  
"""

    elif goal == "Weight Loss":

        return """
### 🍳 Breakfast:
• Vegetable upma  
• Boiled eggs with multigrain toast  
• Poha with peanuts  

### 🍛 Lunch:
• Grilled chicken with brown rice  
• Dal with 2 chapatis and salad  
• Curd rice (small portion)  

### 🍲 Dinner:
• Clear vegetable soup  
• Grilled paneer tikka  
• Moong dal with stir-fried vegetables  
"""

    else:  # Maintain

        return """
### 🍳 Breakfast:
• Idli with sambar  
• Oats porridge with fruits  
• Vegetable omelette  

### 🍛 Lunch:
• Rice with dal and sabzi  
• Chicken curry with 2 chapatis  
• Lemon rice with curd  

### 🍲 Dinner:
• Vegetable khichdi  
• Roti with paneer curry  
• Fish curry with rice  
"""