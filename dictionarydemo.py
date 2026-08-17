d = {101:"khusahi" , 899 : "harsh" , 897 : "karan" , 987:"zeel" , 123: "chaitnay " }

print(d)
print(d[899])
print(d.get(101))
print(d.items())
print(d.keys())
print(d.pop(101))
print(d)
d.popitem()
print(d)
d1 = {876 : " karan" , 567:"manik"}
d.update(d1)
print(d)
print(d.values())

for i in d:
    print(i , " : " , d[i])

for key , value in d.items():
    print(key , " : " , value)    

if  897 in d:
        print("897 is inside already" )
else:
     print("not inside ")
