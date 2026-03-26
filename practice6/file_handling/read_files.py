#Return the 5 first characters of the file:

with open("demofile.txt") as f:
  print(f.read(5))

#Read one line of the file:

with open("demofile.txt") as f:
  print(f.readline())

#Read two lines of the file:

with open("demofile.txt") as f:
  print(f.readline())
  print(f.readline())

#Loop through the file line by line:

with open("demofile.txt") as f:
  for x in f:
    print(x)