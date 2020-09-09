import requests
from bs4 import BeautifulSoup

# CONSTANTS
KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'JavaScript', 'JS']
URL = 'https://habr.com/ru/all/'
NL = '\n'

keywords_lower = [element.lower() for element in KEYWORDS] ; keywords_lower
#print(KEYWORDS, keywords_lower)

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
       if any([hub_lower in desired for desired in keywords_lower]):
           title_element = article.find('a', class_='post__title_link')
           name = title_element.text
           url = title_element.attrs.get('href')
           date_element = article.find('span', class_='post__time')
           date = date_element.text
           print(f'Найдены следующие статьи, которые соответствуют заданным ключевым словам: {date} - {name} - {url}')

           # так как пост уже нам подошел - дальше нет смысла проверять хабы
           break
