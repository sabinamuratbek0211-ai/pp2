#1
x = 1 #Variables of numeric types are created when you assign a value to them:
y = 2.8
z = 1j 
print(type(x)) #To verify the type of any object in Python, use the type() function
print(type(y))
print(type(z))

#2
x = 3+5j #Complex numbers are written with a "j" as the imaginary part
y = 5j
z = -5j
print(type(x))
print(type(y))
print(type(z))


#3
x = 1    # int
y = 2.8  # float
z = 1j   # complex
#convert from int to float:
a = float(x)
#convert from float to int:
b = int(y)
#convert from int to complex:
c = complex(x)
print(a)
print(b)
print(c)
print(type(a))
print(type(b))
print(type(c)) 

#4
x = 1
y = 35656222554887711
z = -3255522

print(type(x))
print(type(y))
print(type(z))


#5 random
import random #Python does not have a random() function to make a random number, but Python has a built-in module called random that can be used to make random numbers:
print(random.randrange(1, 10))
