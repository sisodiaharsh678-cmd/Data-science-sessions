class sample:
    a = 10 

    def __init__(self):
        self.b = 20

    def instance_method(self):
        self.b +=5
        print("instance" , self.b)  

    @classmethod
    def class_method(cls):
        cls.a +=5
        print("class :" , cls.a)

    @staticmethod
    def static_method(x, y):
        print("Static:", x + y)

obj = sample()

obj.instance_method()
sample.class_method()
sample.static_method(3, 4)