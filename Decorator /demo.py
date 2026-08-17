def my_decorator(func):

    def wrapper():
        print("before calling the function")
        func()
        print("after calling the function ")
    return wrapper 

@my_decorator
def say_helllo():
    print("hello tops")

say_helllo()    
    