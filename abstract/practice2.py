from abc import ABC , abstractmethod

class Car(ABC):

    @abstractmethod
    def mileage(self, m):
        pass

    @abstractmethod
    def speed(self, s):
        pass

    @abstractmethod
    def fuel_type(self, f):
        pass

class BMW(Car):

    def show(self):
        print("I am BMW") 

    def mileage(self, m):
        print("BMW Mileage:", m, "km/l")

    def speed(self, s):
        print("BMW Speed:", s, "km/h")

    def fuel_type(self, f):
        print("BMW Fuel Type:", f)

class Audi(Car):

    def show(self):
        print("I am Audi")

    def mileage(self, m):
        print("Audi Mileage:", m, "km/l")

    def speed(self, s):
        print("Audi Speed:", s, "km/h")

    def fuel_type(self, f):
        print("Audi Fuel Type:", f)    

b1 = BMW()
b1.show()
b1.mileage(15)
b1.speed(240)
b1.fuel_type("Petrol")

a1 = Audi()
a1.show()
a1.mileage(14)
a1.speed(250)
a1.fuel_type("Diesel")

