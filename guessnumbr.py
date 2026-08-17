import random

num = random.randint(1,20)

while True:
    guess = int(input("guess a number between 1 - 20 : "))
    if guess==num:
        print("you correct")
        break
    elif guess>num:
        print("greater")
    elif guess<num:
        print("low")    