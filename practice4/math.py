#Write a Python program to convert degree to radian.
import math

degree = float(input("Input degree: "))
radian = degree * math.pi / 180

print("Output radian:", round(radian, 6))

#Write a Python program to calculate the area of a trapezoid.
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

area = (base1 + base2) * height / 2
print("Expected Output:", area)

#Write a Python program to calculate the area of regular polygon.
import math

n = int(input("Input number of sides: "))
side = float(input("Input the length of a side: "))

area = (n * side ** 2) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", int(area) if area.is_integer() else area)

#Write a Python program to calculate the area of a parallelogram.
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))

area = base * height
print("Expected Output:", area)