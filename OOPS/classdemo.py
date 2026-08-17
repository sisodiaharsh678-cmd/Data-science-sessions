class student:

    def getData(self , fname , lname):
        self.f=fname
        self.l=lname

    def putData(self):
        print("first name : " , self.f)    
        print("last name : " , self.l) 

s1 =student()

s1.getData("harsh" , "sisodia")
s1.putData()