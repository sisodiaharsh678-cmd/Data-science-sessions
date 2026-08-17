#Write a Python program to convert a list of tuples into a dictionar

data = [('a', 1), ('b', 2), ('c', 3)]

result = {}

for key , values in data:
    result[key] = values

print(result)


#list into dict

keys = ['a', 'b', 'c']
values = [1, 2, 3]

result = {}

for i in range(len(keys)):
    result[keys[i]]=values[i]

print(result)
