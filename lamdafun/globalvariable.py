def myfun():
    global name 
    print("1st" , name)
    name="python great"
    print("2nd",name)

name="python"
myfun()

print("3rd" , name)