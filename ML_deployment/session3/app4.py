from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)



@app.route('/predict-delivery', methods=['POST'])
def predict_delivery():
    data = request.get_json()
    distance = data['distance']
    order_size = data['order_size']

    prediction = model.predict(np.array([[distance, order_size]]))
    estimated_time = round(prediction[0], 2)

    message = f"Your order will arrive in approximately {estimated_time} minutes. Sit tight!"

    return jsonify({
        "estimated_delivery_time_minutes": estimated_time,
        "message": message
    })