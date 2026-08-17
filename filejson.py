import json

user_data = {}

user_data["name"] = input("enter ur name")
user_data["age"] = input("enter ur age")
user_data["city"] = input("enter ur city")

with open("user_data.json" , "w") as file:
    json.dump(user_data,file,indent=4)

print("data added ")    