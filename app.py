import streamlit as st
from PIL import Image
from calorie_api import get_calories

from modules.auth import create_users_table, register_user, check_login
from modules.food_recognition import predict_food
from modules.health_engine import calculate_bmi, bmi_category, calculate_body_fat, ideal_weight_range
from modules.nutrition_engine import get_nutrition
from modules.recommender import disease_filter, recommend_alternative, meal_plan
from modules.healthy_score import calculate_healthy_score
from modules.healthy_score import calculate_healthy_score
from calorie_api import get_calories   

st.set_page_config(page_title="SmartNutriPlan", layout="wide")

# SESSION STATE 

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None
if "last_confidence" not in st.session_state:
    st.session_state.last_confidence = None

#  LOGIN PAGE 

def login_page():
    st.title("SmartNutriPlan")

    choice = st.selectbox("Select Option", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Register":
        if st.button("Register"):
            if register_user(username, password):
                st.success("Registered Successfully! Please Login.")
            else:
                st.error("Username already exists.")

    if choice == "Login":
        if st.button("Login"):
            if check_login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid Credentials")

# HOME PAGE 

def home_page():
    st.title("Welcome to SmartNutriPlan")

    with st.expander("Food Recognition"):
        uploaded_file = st.file_uploader("Upload Food Image", type=["jpg","jpeg","png"])
        
        if uploaded_file:
            prediction, confidence = predict_food(uploaded_file)

            st.session_state.last_prediction = prediction
            st.session_state.last_confidence = confidence

            st.image(uploaded_file, width=300)
            st.success(f"Predicted: {prediction}")
            st.info(f"Confidence: {confidence:.2f}%")

            # Calorie Integration
            calories = get_calories(prediction)
            st.metric("Estimated Calories", f"{calories} kcal")

    with st.expander("Diet Recommendation"):
        goal = st.selectbox("Select your goal", ["Weight Gain", "Weight Loss", "Maintain"])
        
        if st.button("Get Recommendation"):
            recommendation = meal_plan(goal)

            st.subheader("Recommended Meal Plan")
            st.markdown(recommendation)


            import re
            food_items = re.split(r",|\n", recommendation)

            total_calories = 0
            st.subheader("Calorie Breakdown")

            for food in food_items:
                food = food.strip()

               
                if not food or ":" in food:
                    continue

                cal = get_calories(food)

                if isinstance(cal, (int, float)):
                    total_calories += cal

                st.write(f"{food} - {cal} kcal")

            st.success(f"Total Estimated Calories: {total_calories} kcal")
    

# DASHBOARD PAGE 

def dashboard_page():
    st.markdown("## Health Dashboard")

    if st.session_state.last_prediction:
        prediction = st.session_state.last_prediction
        confidence = st.session_state.last_confidence

        st.success(f"Last Food: {prediction}")
        st.info(f"Confidence: {confidence:.2f}%")

        nutrition = get_nutrition(prediction)
        st.subheader("Nutritional Values")
        st.write(nutrition)

        calories = get_calories(prediction)
        st.metric("Calories (API)", f"{calories} kcal")

        score = calculate_healthy_score(nutrition)
        st.metric("Health Score", f"{score}/100")

        goal = st.selectbox("Select Goal", ["Weight Loss", "Weight Gain", "Maintain"])
        recommendation = recommend_alternative(goal)

        st.subheader("Recommendation")
        st.write(recommendation)

    else:
        st.info("No food analyzed yet.")

# PROFILE PAGE 

def profile_page():
    st.markdown("## Profile Information")
    st.write("Username:", st.session_state.username)

    # Initialize storage
    if "profile_data" not in st.session_state:
        st.session_state.profile_data = None

    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = True

    # ------------------ VIEW MODE ------------------
    if st.session_state.profile_data and not st.session_state.edit_mode:

        data = st.session_state.profile_data

        st.subheader("Saved Details")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Age:**", data["age"])
            st.write("**Height:**", data["height"], "cm")
            st.write("**Weight:**", data["weight"], "kg")
            st.write("**Gender:**", data["gender"])

        with col2:
            st.write("**Diseases:**", ", ".join(data["diseases"]))
            st.write("**Allergies:**", ", ".join(data["allergies"]))

        # Health Analysis
        bmi = calculate_bmi(data["weight"], data["height"])
        category = bmi_category(bmi)
        body_fat = calculate_body_fat(data["age"], bmi, data["gender"])
        ideal_min, ideal_max = ideal_weight_range(data["height"])

        st.markdown("---")
        st.subheader("Health Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("BMI", bmi)
            st.write("Category:", category)

        with col2:
            st.metric("Body Fat % (Est.)", f"{body_fat}%")
            st.write(f"Ideal Weight Range: {ideal_min}kg - {ideal_max}kg")

        if st.button("Edit Profile"):
            st.session_state.edit_mode = True
            st.rerun()

    # ------------------ EDIT MODE ------------------
    else:

        age = st.number_input("Age", 10, 100)
        height = st.number_input("Height (cm)", 100, 220)
        weight = st.number_input("Weight (kg)", 30, 150)
        gender = st.selectbox("Gender", ["Male", "Female"])

        diseases = st.multiselect("Select Diseases", [
            "Hypertension", "Obesity", "Diabetes Type 1", "Diabetes Type 2",
            "Heart Disease", "PCOS", "Thyroid - Hypo", "Thyroid - Hyper",
            "Kidney Disease", "Liver Disease", "Anemia", "High Cholesterol",
            "Gastritis", "Ulcer", "Arthritis", "Asthma", "Celiac Disease",
            "IBS", "Fatty Liver", "None"
        ])

        allergies = st.multiselect("Allergies", [
            "None", "Peanuts", "Tree Nuts", "Milk", "Egg", "Fish", "Shellfish",
            "Soy", "Wheat", "Gluten", "Sesame", "Mustard", "Corn", "Tomato",
            "Potato", "Garlic", "Onion", "Strawberry", "Banana", "Chocolate",
            "Food Colorings", "Preservatives", "MSG", "Lactose"
        ])

        if st.button("Save Profile"):

            st.session_state.profile_data = {
                "age": age,
                "height": height,
                "weight": weight,
                "gender": gender,
                "diseases": diseases,
                "allergies": allergies
            }

            st.session_state.edit_mode = False
            st.success("Profile Saved Successfully!")
            st.rerun()
# MAIN 

def main():
    create_users_table()

    if not st.session_state.logged_in:
        login_page()
    else:
        menu = st.selectbox("", ["Home", "Dashboard", "Profile", "Logout"])

        if menu == "Home":
            home_page()
        elif menu == "Dashboard":
            dashboard_page()
        elif menu == "Profile":
            profile_page()
        elif menu == "Logout":
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()