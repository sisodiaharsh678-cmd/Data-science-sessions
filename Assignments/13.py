#Write a Python program to sort a dictionary (ascending /descending) by value.

my_dict = {"a" : 2 , "b" : 1 , "c" : 5 , "d" : 6 , "e" : 4}

asc_sorted = dict(sorted(my_dict.items() , key=lambda x:x[1]))
desc_sorted = dict(sorted(my_dict.items() , key=lambda x:x[1] , reverse=True))

print("Original Dictionary:", my_dict)
print("Ascending Order:", asc_sorted)
print("Descending Order:", desc_sorted)