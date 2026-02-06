#The child's __init__() function overrides the inheritance of the parent's __init__() function.
class Student(Person):
  def __init__(self, fname, lname):
    #add properties etc.

#To keep the inheritance of the parent's __init__() function, add a call to the parent's __init__() function:

class Student(Person):
  def __init__(self, fname, lname):
    Person.__init__(self, fname, lname)