print("start code")

try:
    a = int(input("enter a : "))
    b = int(input("enter b : "))
    c = a/b
    print("division" , c)
except ZeroDivisionError as e:
    print("exception error : " , e)

print("end code ")    
