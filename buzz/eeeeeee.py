import requests
html = requests.get("https://www.baidu.com")
print(html.text())
