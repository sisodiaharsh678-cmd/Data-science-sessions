def fibonacci(n):
    a,b = 0 , 1
    for i in range(n):
        yield a
        a,b = b , a + b
#create generator 
fib = fibonacci(20)

#iterate and printe the fibonacci numbers
print(fib)
for num in fib:
    print(num,end=" ")
