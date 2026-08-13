import streamlit as st

# ---------------------------------------------------------
# Page setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="Food Delivery Intelligence Dashboard",
    page_icon="🍔",
    layout="wide"
)

# ---------------------------------------------------------
# Home page content
# ---------------------------------------------------------
st.title("🍔 Food Delivery Intelligence Dashboard")

st.markdown(
    """
    Welcome to the **Food Delivery Intelligence Platform** — an end-to-end tool
    combining interactive data exploration, real-time deep learning inference,
    and model transparency for delivery operations teams.

    ### What you can do here
    Use the sidebar on the left to navigate between pages:

    - **📊 Data Explorer** — Upload your delivery CSV data to view summary
      statistics and interactive charts covering hourly order volume and
      delivery time distribution by restaurant.
    - **🤖 Demand Predictor** — Get a live demand forecast (Low / Medium / High)
      from a trained neural network based on hour of day, day of week, and
      temperature.
    - **🧠 Model Info** — Inspect the deployed model's architecture and review
      its training accuracy/loss history.

    ---

    Built with **Streamlit**, **TensorFlow/Keras**, and **Plotly**, this app
    consolidates data visualization and neural network deployment into a single
    production-ready dashboard for a food delivery platform's operations team.
    """
)

st.info("👈 Select a page from the sidebar to get started.")
