import requests
from bs4 import BeautifulSoup
import re

# CONSTANTS
KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'urllib']
URL = 'https://habr.com/ru/all/'
NL = '\n'


# get URL
result = requests.get(URL)
soup = BeautifulSoup(result.text, 'html.parser')

# get articles
articles = soup.find_all('article', class_='post')
for article in articles:
    article_id = article.parent.attrs.get('id')
   # если идентификатор не найден, это что-то странное, пропускаем
    if not article_id:
        continue
    article_id = int(article_id.split('_')[-1])
    #print(NL, 'article:', article_id)

   # get hubs
    hubs = article.find_all('a', class_='hub-link')
    for hub in hubs:
       hub_lower = hub.text.lower()
       #print('hub_lower:', hub_lower)
       # ищем вхождение хотя бы одного желаемого хаба
       if any([hub_lower in desired for desired in KEYWORDS]):
           title_element = article.find('a', class_='post__title_link')
           name = title_element.text
           url = title_element.attrs.get('href')
           date_element = article.find('span', class_='post__time')
           date = date_element.text


           #additional article text check
           article_text = requests.get(url)
           soup_text = BeautifulSoup(article_text.text, 'html.parser')
           #print('***', soup_text)
           is_relative = False
           for key in KEYWORDS:
               key_search = soup.find('div id', text=key)
               result = key_search.next_sibling.strip()
               print(f'+++ {key}: {result}')
               is_relative = True

           if is_relative:
               print(f'Cтатьи, которые соответствуют заданным ключевым словам:{NL} {date} - {name} - {url}')
           else:
               print('Не найдено статей соответствующих заданным ключевым словам')








           # так как пост уже нам подошел - дальше нет смысла проверять хабы
           break
