#The child's __init__() function overrides the inheritance of the parent's __init__() function.
class Student(Person):
  def __init__(self, fname, lname):
    #add properties etc.

#To keep the inheritance of the parent's __init__() function, add a call to the parent's __init__() function:

class Student(Person):
  def __init__(self, fname, lname):
    Person.__init__(self, fname, lname)

#Add a method called welcome to the Student class:
#If you add a method in the child class with the same name as a function in the parent class, the inheritance of the parent method will be overridden.
class Student(Person):
  def __init__(self, fname, lname, year):
    super().__init__(fname, lname)
    self.graduationyear = year

  def welcome(self):
    print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)