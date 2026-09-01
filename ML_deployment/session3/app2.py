from flask import Flask , request , jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Prediction API"

@app.route('/predict-price' , methods=['POST']) 
def predict_price():
    data = request.get_json
    base_price = data['base_price'] 
    discount = data['discount']

    final_price = base_price-(base_price * discount/100)

    return jsonify({"final_price": final_price})

if __name__ == '__main__':
    app.run(debug=True)    