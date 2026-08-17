import re

text = "A1 B22 C333"
result = re.findall(r'\d+' , text)

print(result)