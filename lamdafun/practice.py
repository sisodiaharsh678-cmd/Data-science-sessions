l = [1,2,3,4,5,6,7,8,9,10]

l3 = (filter(lambda x: (x**3) % 2 == 0, l))

print(list(l3))

a=20
b=25

big = lambda x, y: x if x > y else y

print(big(a, b))
