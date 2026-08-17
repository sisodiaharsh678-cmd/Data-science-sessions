import re

text = "A1 B22"
match = re.search(r'\d+',text)

print(match.group())
