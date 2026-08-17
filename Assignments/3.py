#Write a Python program to count the occurrences of each word in a given sentence.

sentence  = input("enter the sentence : ")

words = sentence.split()
count_dict = {}

for word in words:
    word = word.lower()

    if word in count_dict:
        count_dict[word] += 1 
    else:
        count_dict[word] = 1

print("word Count : ")

for key , value in count_dict.items():
    print(key,":" , value)


