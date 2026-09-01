from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)  


with open("review_sentiment_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

@app.route('/')
def home():
    return "Review Sentiment Prediction API is running"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    review_text = data['review']

    review_vector = vectorizer.transform([review_text])
    prediction = model.predict(review_vector)[0]

    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(debug=True)