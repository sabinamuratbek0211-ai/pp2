#1
import re

pattern = r'ab*'
text = "abbb"

if re.fullmatch(pattern, text):
    print("Match found")
else:
    print("No match")

#2
import re

pattern = r'ab{2,3}'
text = "abbb"

if re.fullmatch(pattern, text):
    print("Match found")
else:
    print("No match")

#3
import re

text = "hello_world test_value example"

matches = re.findall(r'[a-z]+_[a-z]+', text)
print(matches)

#4
import re

text = "Hello world This Is Python"

matches = re.findall(r'[A-Z][a-z]+', text)
print(matches)

#5
import re

pattern = r'a.*b'
text = "axxxb"

if re.fullmatch(pattern, text):
    print("Match found")
else:
    print("No match")

#6
import re

text = "Hello, world. Python is great"

result = re.sub(r'[ ,.]', ':', text)
print(result)

#7
def snake_to_camel(text):
    words = text.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])

text = "hello_world_python"
print(snake_to_camel(text))

#8
import re

text = "HelloWorldPython"

result = re.split(r'(?=[A-Z])', text)
print(result)

#9
import re

text = "HelloWorldPython"

result = re.sub(r'([A-Z])', r' \1', text).strip()
print(result)

#10
import re

text = "helloWorldPython"

result = re.sub(r'([A-Z])', r'_\1', text).lower()
print(result)
