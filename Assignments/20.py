import random 
import string 

class User:
    def __init__(self,user_id,name,password):
        self.user_id=user_id
        self.name=name
        self.password=password

    def get_details(self):
        return(self.user_id , self.name , self.password)


def generate_password(user_input):
    try:
        if not user_input.strip():
            raise ValueError("Input cannnot be empty") 

        words = user_input.split()
        if len(words)==0:
            raise ValueError("Please enter at least one Word")

        password_words = random.sample(words , min(2,len(words))) 
        password = ''.join(password_words)

        password += str(random.randint(10,99))

        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>/?"
        password += random.choice(special_chars)
        
        while len(password)<8:
            password += random.choice(string.ascii_letters + string.digits+special_chars)

        return password
    
    except Exception as e:
        print(f"Error generating password: {e}")
        return None

users = []

try:

        n = int(input("Enter number of users : "))
        for i in range(n):
            print(f"\n--- Enter details for User---")
            user_id = input("User ID: ")
            name = input("Name: ")
            user_input = input("Enter some words to generate password: ")  

            password = generate_password(user_input)
            if password:
                user=User(user_id , name , password)
                users.append(user)
                print(f"Generated password for {name}:{password}")
            else:
                print("Password cannot be generated")   
except ValueError:
      print("please enter a valid number for user input")

except Exception as e:
        print(f"Unexpected error : {e}")

print("\n All User Details")
for user in users:
    print(user.get_details())    


        