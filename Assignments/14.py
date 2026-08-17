#Write a Python program to find the highest 3 values in a dictionary.

my_dict = {'a': 50, 'b': 75, 'c': 30, 'd': 90, 'e': 60}

sorted_items = sorted(my_dict.items() , key=lambda x:x[1] , reverse=True)

top3 = dict(sorted_items[:3])

print("top 3 values",top3)




