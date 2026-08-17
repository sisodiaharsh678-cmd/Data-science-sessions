d = {1:"jigar" , 2:"jay" , 3:"vijay" , 4:"kamal" , 5:"ketan"}

key = int(input("Enter existing key. :"))
value = input("enter new value :")

if key in d:
    d[key]= value
else:
    print("key is not presented in dic")

print(d)        