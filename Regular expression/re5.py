import re

t = "A1 B22"
result = re.sub(r'\d+' , 'X' , t)

print(result)