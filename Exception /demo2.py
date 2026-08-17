print("start code ")

try:
    a = int(input("enter the number : "))
    b = int(input("enter the number : "))
    c = a/b
    print("division" , c)
    l=[10,20,30,40,50]
    index = int(input("enter index number to each element :"))
    print("elemtent : " , l[index])
except ZeroDivisionError as e:
    print("Exception caught : " , e)   
except      