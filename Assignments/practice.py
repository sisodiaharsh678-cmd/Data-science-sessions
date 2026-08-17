str1 = input("Enter first string: ")
str2 = input("Enter second string: ")

mid = len(str1)//2
result = str1[:mid] + str2 + str1[mid:]
print(result)
