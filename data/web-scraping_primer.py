# определяем список хабов, которые нам интересны
DESIRED_HUBS = ['дизайн', 'физика', 'web', 'python', 'программирование']

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

header = Headers(
    browser="chrome",  # Generate only Chrome UA
    os="win",  # Generate ony Windows platform
    headers=True  # generate misc headers
)


# получаем страницу с самыми свежими постами
ret = requests.get('https://habr.com/ru/all/',headers=header.generate())
print(ret)
soup = BeautifulSoup(ret.text, 'html.parser')

# извлекаем посты
posts = soup.find_all('article', class_='post')
print((posts))
for post in posts:
   post_id = post.parent.attrs.get('id')
   # если идентификатор не найден, это что-то странное, пропускаем
   if not post_id:
       continue
   post_id = int(post_id.split('_')[-1])
   print('post', post_id)

   # извлекаем хабы поста
   hubs = post.find_all('a', class_='hub-link')
   for hub in hubs:
       hub_lower = hub.text.lower()
       # ищем вхождение хотя бы одного желаемого хаба
       if any([hub_lower in desired for desired in DESIRED_HUBS]):
           # пост нам интересен - делаем с ним все что захотим:
           # можно отправит в телеграм уведомление, можно на почту и т.п.
           title_element = post.find('a', class_='post__title_link')
           print(title_element.text, title_element.attrs.get('href'))

           # так как пост уже нам подошел - дальше нет смысла проверять хабы
           break