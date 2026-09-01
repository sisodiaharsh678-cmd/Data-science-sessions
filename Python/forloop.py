"for loop"


for i in range (10):
    print(i)
print("------------------------")    

for i in range (3,10):
    print(i)
print("------------------------") 

for i in range (1,10,3):
    print(i)
print("------------------------")  

for i in range (110,0,-1):
    print(i)
print("------------------------") 

for i in range(1,10):
    for j in range(1 , i+1):
        print("*" , end = " ")
print()        






for i in range (1 , 10):
    print(" " * (9-i) , "*"*i)

print("------------------------")

for i in range (1 , 10):
    print(" " * (9-i) , " *"*i)    

print("------------------------")    

for i in range(1, 10):
    for j in range(1, i + 1):
        print(j, end=" ")
    print()

print("------------------------")

for i in range(1, 10):
    for j in range(1, i + 1):
        print(i, end=" ")
    print()

print("------------------------")

for i in range(65 , 75):
    for j in range(65 , i + 1):
        print(chr(i), end=" ")
    print()    

print("------------------------")

for i in range(65 , 75):
    for j in range(65 , i + 1):
        print(chr(j), end=" ")
    print() 

print("------------------------")

for i in range (2000 , 3201):
    if i%5==0 and i%7!=0:
        print(i , end=" ")

