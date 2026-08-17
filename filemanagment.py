file = open("tops1.txt" , "w")
file.write("this is file management demo python")
file.close()
print("file written successfully")

print("*" , 50)

file=open("tops1.txt" , "r")
print(file.read())
file.close()

print("*" , 50)

file = open("tops.txt" , "a")
file.write("\nNow this file append")
file.close()

print("*" , 50)

file= open("tops1.txt","r")
print(file.read())
file.close()

file = open("tops2.txt" , "w+")
file.write("this is file management demo python 2")
file.seek(0)
print(file.read())

file.close()