#Write a Python program to add 'ing' at the end of a given string (length should be at least 3).
#If the given string already ends with 'ing' then add 'ly' instead If the string length of the given
#string is less than 3, leave it unchanged

s= input("enter the string : ")

if len(s) >= 3 :
    if s.endswith("ing"):
        s = s + "ly"
    else:
        s = s + "ing"

print("final string : " , s)            