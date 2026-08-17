#swap first n last ch

s = input("enter the string")

if len(s) >= 2 :
    s = s[-1]  + s[1:-1] + s[0]
print("result " , s)    