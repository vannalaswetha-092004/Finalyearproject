import os
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "smartnutriplan_food_model.keras")
CLASS_PATH = os.path.join(BASE_DIR, "..", "models", "class_names.txt")

model = load_model(MODEL_PATH)

with open(CLASS_PATH, "r") as f:
    class_names = [line.strip() for line in f.readlines()]

def predict_food(uploaded_file):
    img = Image.open(uploaded_file)
    img = img.resize((224, 224))
    img = img.convert("RGB")

    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)

    predicted_index = np.argmax(predictions)
    confidence = float(np.max(predictions)) * 100

    predicted_label = class_names[predicted_index]

    return predicted_label, confidence