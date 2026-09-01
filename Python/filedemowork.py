import random 

data = open("data.txt" , "w")
for i in range(10):
    data.write(str(random.randint(1,100)) + ",")
data.close()

data = open("data.txt","r")
even = open("even.txt" , "w")
odd = open("odd.txt" , "w")
prime = open("prime.txt","w")

l = data.read().split(",")[:-1]

for i in l:
    n = int(i)

    
    if n % 2 == 0:
        even.write(i + ",")
    else:
        odd.write(i + ",")

   
    c = 0
    for j in range(1 , n+1):
        if n % j == 0:
            c += 1

    if c == 2:
        prime.write(i + ",")

data.close()
even.close()
odd.close() 
prime.close()