def count_up_to(n):
    count = 1
    while count <= n:
        yield count
        count += 1

#create a generator object 
counter = count_up_to(5)

#iterate over the generator 
for num in counter:
    print(num)

def simple_generator():
    num=1
    while num<1000:
        yield num
        num=num+100

g =simple_generator()

print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))


             
    