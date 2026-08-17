import string

def check_password(password):
    try:
        if len(password) < 8:
            return "Weak Password"
        
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special= any(c in string.punctuation for c in password)

        if has_upper and has_digit and has_special:
            return "Strong Passsword"
        else:
            return "Weak Password"
        
    except Exception as e :
        print(e)

pwd = input("Enter password: ")
print(check_password(pwd))   
