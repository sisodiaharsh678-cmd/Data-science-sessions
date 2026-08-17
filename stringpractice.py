text = input("Enter a string: ")

upper_count = 0
lower_count = 0
number_count = 0
space_count = 0

for char in text:
    if char.isupper():
        upper_count += 1
    elif char.islower():
        lower_count += 1
    elif char.isdigit():
        number_count += 1
    elif char.isspace():
        space_count += 1

print("Uppercase letters :", upper_count)
print("Lowercase letters :", lower_count)
print("Numbers           :", number_count)
print("Spaces            :", space_count)