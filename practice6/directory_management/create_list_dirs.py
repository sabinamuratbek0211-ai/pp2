#Create nested directories
import os
os.makedirs("parent/child/grandchild", exist_ok=True)

#List files and folders
import os
print(os.listdir("."))  # current directory

#Find files by extension
import os

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".txt"):
            print(os.path.join(root, file))


