

d = {1:10 , 2:15 , 3:20 , 4:16 , 5:8 , 6:12 , 7:34 , 8:9 , 9:10 , 10:15}

even_sum=0
odd_sum = 0

for v in d.values():
    if v % 2 == 0:
        even_sum += v
    else:
        odd_sum += v

print("Dictionary:", d)
print("Even Sum:", even_sum)
print("Odd Sum:", odd_sum)
