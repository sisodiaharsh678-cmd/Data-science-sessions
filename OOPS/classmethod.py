class student:
    subject = "python"

    @classmethod
    def get_subject(cls):
        return cls.subject
    
    @classmethod
    def set_subject(cls , new_subject):
        cls.subject = new_subject

#calling class method
print(student.get_subject())

#modifying class attribute using class method
student.set_subject("flutter")
print(student.get_subject())

