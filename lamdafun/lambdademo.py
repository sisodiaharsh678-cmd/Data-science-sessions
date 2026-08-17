x = lambda a,b,c:a+b+c
print(x(20,30,23))

result = lambda num : "even" if num%2==0 else "odd"

print(result(13))


#l=[1,2,3,4,5,6,7,8,9,10]
#even=[]

#11= filter(lamda x:x%)


l = [1,2,3,4,5,6,7,8,9,10]

result = (filter(lambda x: (x**3) % 2 == 0, l))

print(list(result))