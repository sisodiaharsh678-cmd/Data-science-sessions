import re

text = "Hello hello HELLO"
result = re.findall(r'hello', text, re.I)

print(result)