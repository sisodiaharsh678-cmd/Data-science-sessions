from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("delivery_time_model.joblib")

@app.route('/')
def home():
    return "welcom to the api"

@app.route('/predict-price' ,methods=['POST'])
def predict_price():
    data = request.get_json()
    base_price = data['base_price']
    discount = data['discount']
    final_price = base_price - (base_price * discount / 100)
    return jsonify({"final_price": final_price})

@app.route('/predict-delivery', methods=['POST'])
def predict_delivery():
    data = request.get_json()
    distance = data['distance']
    order_size = data['order_size']

    prediction = model.predict(np.array([[distance, order_size]]))
    estimated_time = round(prediction[0], 2)

    return jsonify({"estimated_delivery_time_minutes": estimated_time})

if __name__ == '__main__':
    app.run(debug=True)    