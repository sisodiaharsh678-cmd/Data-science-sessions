#Write a python program using function to find the sum of odd series and even series


def factorial(n):
    fact = 1 
    for i in range(1 , n+1):
        fact *= i
    return fact 

def series_sum(n , series_type):
    total = 0
    start = 1 if series_type == "odd" else 2
    for i in range(start , n+1 , 2):
        total += (i ** 2)/factorial(i)
    return total  


n=10       

odd_sum = series_sum(n, "odd")
even_sum = series_sum(n, "even")

print(f"Sum of odd series up to {n}: {odd_sum}")
print(f"Sum of even series up to {n}: {even_sum}")



