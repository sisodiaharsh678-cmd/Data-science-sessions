class student:
    def sample(self , name , age):
        self.name = name
        self.age = age 

    def describe(self):
        return f'{self.name} is {self.age} years old'

student = student()
student.sample("jigar" , 40)
print(student.describe())            