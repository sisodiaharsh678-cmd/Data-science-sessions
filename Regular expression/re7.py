import re

m = re.search(r'\d+', "A123B")

print(m.group())
print(m.start())
print(m.end())
print(m.span())