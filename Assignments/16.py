#Counting the frequencies in a list using a dictionary in Python.

list = [1, 1, 1, 5, 5, 3, 1, 3, 3, 1,4, 4, 4, 2, 2, 2, 2]

dict = ()

for num in list:
    if num in dict:
        dict[num] += 1
    else:
        dict[num] = 1

print(dict)
