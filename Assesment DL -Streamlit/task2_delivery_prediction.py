import streamlit as st
import joblib
import numpy as np


st.set_page_config(page_title="Delivery Time Prediction", layout="centered")
st.title("🚴 Delivery Time Prediction")


@st.cache_resource
def load_model():
    model = joblib.load("delivery_model.pkl")
    return model


try:
    model = load_model()
    model_loaded = True
except Exception as e:
    st.error(f"Failed to load model file: {e}")
    model_loaded = False

if model_loaded:
    st.subheader("Enter Order Details")

    
    distance = st.slider("Distance (km)", min_value=1, max_value=50, value=10)
    order_value = st.number_input("Order Value (Rs)", min_value=0.0, value=500.0, step=10.0)
    time_of_day = st.selectbox("Time of Day", ["Morning", "Afternoon", "Evening", "Night"])

    
    time_mapping = {"Morning": 0, "Afternoon": 1, "Evening": 2, "Night": 3}

    if st.button("Predict Delivery Time"):
        try:
            time_encoded = time_mapping[time_of_day]
            features = np.array([[distance, order_value, time_encoded]])

            prediction = model.predict(features)[0]

            st.success(f"Estimated Delivery Time: {prediction:.1f} minutes")

        except ValueError as ve:
            st.error(f"Invalid input values: {ve}")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
