import re

text = "A1 B22"

for m in re.finditer(r'\d+', text):
    print(m.group(), m.start(), m.end())