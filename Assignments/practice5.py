import random 


def generate_username(name):
    try:
        if not name.strip():
            raise ValueError("Name cannot be empty")
        
        name_part = name[:3]
        number = random.randint(100,999)
        special = random.choice("@#$")

        username = name_part + str(number) + special
        return username
    
    except Exception as e:
        print(e)

name = input("Enter name: ")
print("Username:", generate_username(name))        