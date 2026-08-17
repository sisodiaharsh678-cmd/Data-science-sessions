#Write a Python program to unzip a list of tuples into individual lists.

data = [(1 , "a") , (2 , "b") , (3 , "c")]

nums = []
chars = []

for x , y in data:
    nums.append(x)
    chars.append(y)

print("Numbers : " , nums)
print("chars: ",chars)    