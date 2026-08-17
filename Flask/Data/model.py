import pickle 

#load trained model 

with open("pass_predictor.pkl", "rb") as file:
    model = pickle.load(file)


def predict_student(study_hours,attendance):

    prediction = model.predict([
        [hours_studied, attendance, previous_score]
    ])

    return int(prediction[0])