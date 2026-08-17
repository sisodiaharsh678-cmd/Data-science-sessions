roll = int(input("Enter ur roll number : "))
snme = input("Enter name : ")
s1 = int(input("enter marks of subject 1 : "))
s2 = int(input("enter marks of subject 2 : "))
s3 = int(input("enter marks of subject 3 : "))

total = s1 + s2 + s3 
per = total/3

print ("roll no : " , roll)
print("student name : " , snme)
print("total : " , total)
print("per :" , per)

if per>=70: 
    print("distinction")
elif    per>=60:
    print("first class")
elif    per>=50:
    print("second class")
elif    per>=40:
    print("pass class")    
else:
    print("fail")    

