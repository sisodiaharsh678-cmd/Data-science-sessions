n = int(input("enter the number  :  "))
rev = 0 

while n>0:
    digit = n % 10
    rev = rev * 10 + digit
    n= n // 10

print("reversed number : " , rev)    


n = int(input("enter the number  :  "))
sum_digit = 0 

while n> 0 :
    digit = n % 10 
    sum_digit += digit 
    n = n//10 
print(sum_digit)    
