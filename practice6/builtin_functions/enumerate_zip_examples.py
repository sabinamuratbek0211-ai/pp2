#Convert a tuple into an enumerate object:

x = ('apple', 'banana', 'cherry')
y = enumerate(x)
print(list(y))

#Join two tuples together: zip
a = ("John", "Charles", "Mike")
b = ("Jenny", "Christy", "Monica")

x = zip(a, b)

#use the tuple() function to display a readable version of the result:

print(tuple(x))

#If one tuple contains more items, these items are ignored:

a = ("John", "Charles", "Mike")
b = ("Jenny", "Christy", "Monica", "Vicky")

x = zip(a, b)