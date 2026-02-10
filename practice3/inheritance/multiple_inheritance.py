class Parent1:
    def method1(self):
        print("Method from Parent1")

class Parent2:
    def method2(self):
        print("Method from Parent2")

# Child inherits from both Parent1 and Parent2
class Child(Parent1, Parent2):
    def child_method(self):
        print("Method from Child")

c = Child()
c.method1()        # from Parent1
c.method2()        # from Parent2
c.child_method()   # from Child


#2
class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")

class C(A):
    def show(self):
        print("C")

class D(B, C):
    pass

d = D()
d.show()  # Output: B
