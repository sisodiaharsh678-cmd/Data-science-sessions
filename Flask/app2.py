from flask import Flask , jsonify , request

app = Flask(__name__)

@app.route("/",methods = ["GET"])
def home():
    return jsonify(
        {
            "massage" : "student management system",
            "status" : "API is runnig"
        }
    )

students = [
    {
        "id" : 1 , 
        "name" : "Ram",
        "Age" : 25,
        "city" : "Ahm"
    },
     {
        "id" : 2 , 
        "name" : "syam",
        "Age" : 24,
        "city" : "surat"
    },
     {
        "id" : 3 , 
        "name" : "Dhaval",
        "Age" : 21,
        "city" : "Baroda"
    }
]    

@app.route("/students",methods = ["GET"])
def get_students():
    return jsonify(
        {
            "massage" : "ALl my students",
            "status" : "API is runnig"
        }
    )

@app.route("/students/<int:student_id>",methods = ["GET"])
def get_students1(student_id):
    for i in students:
        if i["id"]==student_id:
            return jsonify(i)


    return jsonify(
        {
            "massage" : "ALl my students",
            "status" : "API is runnig"
        }
    )   

@app.route("/students",methods = ["POST"])
def add_students(): 
    try:
        data = request.get_json()
        new_student = {
            "id":len(students)+1,
            "name":data["name"],
            "age":data["age"],
            "city":data["city"]
        }  
        students.append(new_student)
        return jsonify({
            "message":"student add update",
            "status":new_student
        })
    except Exception as e:
        return jsonify({
            "message": "something went wrong",
            "error": str(e)
        }), 400




if __name__ == "__main__":
     app.run(debug=True)