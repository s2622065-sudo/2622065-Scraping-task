import requests

url = 'http://www.musashino-u.ac.jp'

res = requests.get(url)
res.encoding = 'utf-8'

print(res.text)

with open('musaashino-u.html','w') as f:
    f.write(res.text)