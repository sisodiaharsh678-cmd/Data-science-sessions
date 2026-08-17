class A:
    def getA(self, a):
        self.a = a
    def putA(self):
        print("A =", self.a)

class B(A):
    def getB(self, b):
        self.b = b
    def putB(self):
        print("B =", self.b)

class C(A):
    def getC(self, c):
        self.c = c
    def putC(self):
        print("C =", self.c)

b1 = B()
b1.getA(10)
b1.putA()     
b1.getB(20)
b1.putB()     

c1 = C()
c1.getA(10)
c1.putA()     
c1.getC(30)
c1.putC()