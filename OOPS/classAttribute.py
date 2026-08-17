class car:
    wheels = 4 # class attribute

    def sample(self,brand , model):
        self.brand = brand
        self.model = model

car1 = car()
car2=  car()        

car1.sample("toyoya" , "camry")
car2.sample("honda" , "civic")

print(car1.wheels)
print(car2.wheels)

print("brand with car1 : " , car1.brand)
print("brand with car2 : " , car2.brand)