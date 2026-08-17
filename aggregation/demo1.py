class Department:
    def __init__(self,name):
        self.name = name

    def display_info(self):
        return f"Department : {self.name}"

class University:
    def __init__(self,name):
        self.name=name
        self.departments = []

    def add_department(self,deparment):
        self.departments.append(deparment)

    def display_departments(self):
        print(f"Departments in {self.name} university : ")
        for department in self.departments:   
            print(department.display_info())

department1= Department("computer science")  
department2= Department("electrical engineering")  
department3= Department("mechanical engineering")  

University = University("tech university")

University.add_department(department1)
University.add_department(department2)
University.add_department(department3)

University.display_departments()