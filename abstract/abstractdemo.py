from abc import ABC , abstractmethod

class RBI(ABC):
    @abstractmethod
    def roi(r):
        pass

class SBI(RBI):

    def show(self):
        print("I am SBI")
    def roi(self,r):
        print("Rate of interest given by SBI is : ",r)

class HDFC(RBI):

    def show(self):
        print("I am HDFC")
    def roi(self,r):
        print("Rate of interest given by HDFC is : ",r) 

s1 = SBI()
s1.show()
s1.roi(6.5)

h1 = HDFC()
h1.show()
h1.roi(6.5)
