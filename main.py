import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import re

KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'авто']
str_KW = '|'.join(KEYWORDS)

header = Headers(
    browser="chrome",  # Generate only Chrome UA
    os="win",  # Generate ony Windows platform
    headers=True  # generate misc headers
)

# получаем страницу с самыми свежими постами
url = 'https://habr.com'
ret = requests.get(url + '/ru/all/', headers=header.generate())

soup = BeautifulSoup(ret.text, 'html.parser')

posts = soup.find_all(class_='tm-articles-list__item')
for post in posts:
    time = post.find(class_='tm-article-snippet__datetime-published').next.attrs['title']
    Title = post.find(class_='tm-article-snippet__title-link').next.text
    text = post.find(class_="article-formatted-body article-formatted-body article-formatted-body_version-2").text
    href = post.find(class_="tm-article-snippet__readmore").attrs['href']
    search = re.search(pattern=str_KW, string=text, flags=re.IGNORECASE)
    if search is not None:
        print(f'<{time}> - <{Title}> - <{url + href}>')
