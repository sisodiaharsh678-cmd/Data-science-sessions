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
        "age" : 25,
        "city" : "Ahm"
    },
     {
        "id" : 2 , 
        "name" : "syam",
        "age" : 24,
        "city" : "surat"
    },
     {
        "id" : 3 , 
        "name" : "Dhaval",
        "age" : 21,
        "city" : "Baroda"
    }
]    

@app.route("/students", methods=["POST"])
def add_students():
    try:
        data = request.get_json()
        new_student = {
            "id": len(students) + 1,
            "name": data["name"],
            "age": data["age"],
            "city": data["city"]
        }
        students.append(new_student)

        return jsonify({
            "message": "student added successfully",
            "status": new_student
        })

    except Exception as e:
        return jsonify({
            "message": "something went wrong",
            "error": str(e)
        }), 400

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

@app.route("/students/<int:student_id>", methods=["PUT"])
def update_students(student_id):
    try:
        data = request.get_json()
        print("STUDENT ID FROM URL:", student_id)
        print("DATA RECEIVED:", data)

        for student in students:
            if student["id"] == student_id:
                student["name"] = data["name"]
                student["age"] = data["age"]
                student["city"] = data["city"]
                print("UPDATED STUDENT:", student)

                return jsonify({
                    "message": "student updated successfully",
                    "status": student
                })

        print("NO MATCH FOUND FOR ID:", student_id)
        return jsonify({"message": "student not found"}), 404

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"message": "something went wrong", "error": str(e)}), 400

@app.route("/students/<int:student_id>", methods=["PATCH"])
def patch_student(student_id):
    try:
        data = request.get_json()

        for student in students:
            if student["id"] == student_id:
                # Only update fields that were actually sent
                if "name" in data:
                    student["name"] = data["name"]
                if "age" in data:
                    student["age"] = data["age"]
                if "city" in data:
                    student["city"] = data["city"]

                return jsonify({
                    "message": "student patched successfully",
                    "status": student
                })

        return jsonify({
            "message": "student not found"
        }), 404

    except Exception as e:
        return jsonify({
            "message": "something went wrong",
            "error": str(e)
        }), 400


if __name__ == "__main__":
     app.run(debug=True) 