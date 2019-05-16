import re
str = '1233.sadasd.123141'
result = re.findall(r'\d+',str)
print(result)