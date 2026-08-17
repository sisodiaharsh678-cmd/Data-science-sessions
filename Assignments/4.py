#Write a Python program to get a single string from two given strings, separated by a space and swap the first
#two characters of each string.

str1 = input("enter the first string. :")
str2 = input ("enter the second string  :")

if len(str1) >= 2 and len(str2) >=2 :
    new_str1 = str2[:2] + str1[2:]
    new_str2 = str1[:2] + str2[2:]

else:
    new_str1 = str2 + str1
    new_str2 = str1 + str2

result = new_str1 + " " + new_str2

print("final string : " , result )