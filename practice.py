#random number 10 total in list between 1. to 1000 even number in new list odd in new list 
import random

l = random.sample(range(1,1001), 10)


even_list=[]
odd_list=[]

for i in range(1,1001):
    if i % 2 == 0:
        even_list.append(i)
    else:
        odd_list.append(i)

print("even numbers : " , even_list)
print("odd_numbers :", odd_list)            



even_list = list(range(2,1001,2))
odd_list = list(range(1,1000,2))

print("Random List:", l)
print("even numbers : " , even_list)
print("odd_numbers :", odd_list)            
