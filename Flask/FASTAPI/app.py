from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# FastAPI Object
app = FastAPI()

# Load Trained Model
model = joblib.load("salary_model.joblib")

# Input Schema
class Employee(BaseModel):
    experience: float

# Home Route
@app.get("/")
def home():
    return {
        "message": "Salary Prediction API Running abc and welcome Harsh"
    }   

# Prediction Route
@app.post("/predict")
def predict_salary(data: Employee):
    exp = np.array([[data.experience]])

    prediction = model.predict(exp)

    return {
        "experience": data.experience,
        "predicted_salary": float(prediction[0])
    }