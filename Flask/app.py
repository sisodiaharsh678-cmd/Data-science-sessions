from flask import Flask , jsonify , request
from model import predict_student 
app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(
        {
            "massage" : "student result API",
            "status" : "API is runnig"
        }
    )


@app.route("/predict",method=["Post"])
def predict():
    try:
        data = request.get_json()
        study_hour = data["study_hour"]
        attendance = data["attendance"]
  
        prediction = predict_student(study_hour,attendance)

        if prediction == 1:
             result = "Pass"
        else:
             result = "Fail"  


        return jsonify(
            {
                "study_hour":study_hour,
                "attendance":attendance,
                "prediction":result
            }
        )     
    except Exception as e:
        return jsonify({
            "error" : str(e)
        }),400   

if __name__ == "__main__":
     app.run(debug=True)