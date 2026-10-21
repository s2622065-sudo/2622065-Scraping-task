import requests
from bs4 import BeautifulSoup

url = 'https://www.musashino-u.ac.jp'
res = requests.get(url)

print(f"ステータスコード:{res.status_code}")
print(f"ステータスメッセージ:{res.reason}")

html_soup = BeautifulSoup(res.content,'html.parser')
print(f"html_soupの型:{type(html_soup)}")

h2 = html_soup.find('h2')
print(type(h2))
print(h2)

h2_all = html_soup.find_all('h2')

for h2 in h2_all:
    if h2.span is not None:
        print(h2.span.string)

tag_a_span_list = html_soup.find_all(['a','span'],limit=5)

for tag in tag_a_span_list:
    print(tag)

tag_href_list = html_soup.find_all(attrs={"href":'/'})
for tag in tag_href_list:
    print(tag)

print(html_soup.find_all(id='footer'))
print(html_soup.find_all(class_='l-header'))