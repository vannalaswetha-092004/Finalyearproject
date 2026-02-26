from modules.food_recognition import predict_food

food, confidence = predict_food("test.jpg")
print("Predicted:", food)
print("Confidence:", confidence)