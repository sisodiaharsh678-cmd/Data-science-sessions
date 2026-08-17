d = {1:5, 2:3, 3:5, 4:2, 5:3, 6:7, 7:5, 8:2, 9:1, 10:3}

count = {}

for v in d.values():
    if v in count:
        count[v] += 1
    else:
        count[v] = 1

print(count)