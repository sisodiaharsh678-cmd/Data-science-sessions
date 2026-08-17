#Write a Python program to count occurrences of a substring in a string.

text = input("Enter a string")

substring = input("enter the substring to count :  ")

count = text.count(substring)

print(f"The substring '{substring}' appears {count} times in the string.")

