n =7 

fib_series = [0 , 1]

for i in range(2,n):
    next_sum = fib_series[i-1]+fib_series[i-2]
    fib_series.append(next_sum)

print("first few fibpnacci numbers are :","," .join(map(str,fib_series)))    