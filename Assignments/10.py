#Write a Python program to get unique values from a list.

n = [1,2,1,3,4,5,6]
unique_value = []

for num in n:
    if n.count(num) == 1:
        unique_value.append(num)
print(unique_value)   

#max number
n = [10,20,4,45,99]

first = second = float('-inf')

for num in n:
    if num > first:
        second = first
        first = num
    elif num > second and num != first:
        second=num
print(second)             
       

#min value       
n = [8,3,5,1,9]

min_value = n[0]

for num in n:
    if num<min_value:
       num=min_value
print(min_value)    


