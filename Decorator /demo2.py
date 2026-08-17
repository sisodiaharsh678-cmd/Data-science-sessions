def validate_name_and_contact(func):
    def wrapper(name , contact_number):
        if not name or not isinstance(name , str):
            return "name must be a non-empty string"
        if len(contact_number) != 10 or not contact_number.isdigit():
            return "contact number must be in 10 digit"
        return func(name , contact_number)
    return wrapper


@validate_name_and_contact
def register_user(name , contact_number):
    return f"user {name} with contsct number {contact_number} has been sucessfully registerd"

print(register_user("alice" , "1234567891"))
print(register_user("" , "1234567891"))
print(register_user("alice" , "12345"))
print(register_user("" , "123456abc"))
