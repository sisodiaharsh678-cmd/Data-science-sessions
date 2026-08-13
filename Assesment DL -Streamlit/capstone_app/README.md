# Food Delivery Intelligence Dashboard

A multi-page Streamlit application combining interactive delivery data exploration, real-time neural network demand prediction, and model transparency into a single deployable platform.

## How to Run Locally

1. Make sure `demand_model.keras` (the trained model from Task 3) and `training_history.pkl` (the saved training history) are placed in this same folder as `Home.py`.
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the app from this folder:
   ```bash
   streamlit run Home.py
   ```
4. Your browser will open automatically to `http://localhost:8501`. Use the sidebar to navigate between the Home, Data Explorer, Demand Predictor, and Model Info pages.
