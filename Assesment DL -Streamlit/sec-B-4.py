import streamlit as st
import numpy as np
import tensorflow as tf
import plotly.graph_objects as go


st.set_page_config(page_title="Demand Predictor", layout="centered")
st.title(" Food Delivery Demand Predictor")


@st.cache_resource
def load_model():
    return tf.keras.models.load_model("demand_model.keras")

try:
    model = load_model()
    model_loaded = True
except Exception as e:
    st.error(f"Failed to load model: {e}")
    model_loaded = False

if model_loaded:
    st.subheader("Enter Conditions")

   
    hour = st.slider("Hour of Day", min_value=0, max_value=23, value=12)

    day_options = ["Monday", "Tuesday", "Wednesday", "Thursday",
                   "Friday", "Saturday", "Sunday"]
    day_label = st.selectbox("Day of Week", day_options)
    day_encoded = day_options.index(day_label)  

    temperature = st.number_input(
        "Temperature (°C)", min_value=10.0, max_value=45.0, value=25.0, step=0.5
    )

    class_names = ["Low", "Medium", "High"]

    

    if st.button("Predict Demand"):
        try:
           
            features = np.array([[hour, day_encoded, temperature]])

            probabilities = model.predict(features)[0]   # shape (3,)
            predicted_idx = int(np.argmax(probabilities))
            predicted_class = class_names[predicted_idx]
            confidence = probabilities[predicted_idx] * 100

            if predicted_class == "High":
                st.warning(
                    f" Predicted Demand: **{predicted_class}** "
                    f"({confidence:.1f}% confidence) — prepare for a surge."
                )
            else:
                st.success(
                    f"Predicted Demand: **{predicted_class}** "
                    f"({confidence:.1f}% confidence)"
                )

            
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=class_names,
                        y=[p * 100 for p in probabilities],
                        marker_color=["#4CAF50", "#FFC107", "#F44336"],
                        text=[f"{p*100:.1f}%" for p in probabilities],
                        textposition="outside"
                    )
                ]
            )
            fig.update_layout(
                title="Prediction Confidence by Class",
                xaxis_title="Demand Class",
                yaxis_title="Probability (%)",
                yaxis_range=[0, 100]
            )
            st.plotly_chart(fig, use_container_width=True)

        except ValueError as ve:
            st.error(f"Invalid input values: {ve}")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
