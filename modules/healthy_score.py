def calculate_healthy_score(nutrition_data):

    # If nutrition is None → return 0
    if nutrition_data is None:
        return 0

    score = 100

    if nutrition_data.get("calories", 0) > 500:
        score -= 20

    if nutrition_data.get("fat", 0) > 20:
        score -= 15

    if nutrition_data.get("carbs", 0) > 60:
        score -= 15

    return max(score, 0)