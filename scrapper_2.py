import requests
from bs4 import BeautifulSoup

# CONSTANTS
KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'urllib', 'JavaScript', 'JS', 'CRM', 'Rocket']
URL = 'https://habr.com/ru/all/'
NL = '\n'
interesting_articles = [] #save here passed filter articles

keywords_lower = [element.lower() for element in KEYWORDS];
print('Ищем по следующим ключевым словам: ', keywords_lower)

# get URL
result = requests.get(URL)
soup = BeautifulSoup(result.text, 'html.parser')


# get articles
articles2 = soup.find_all('article', class_='post post_preview')
intext_words = []  # save here keywords from article text
for article in articles2:
    #print('+++', article)
    for word in KEYWORDS:
        if word.lower() in article.text.lower():
            is_relative = True
            intext_words.append(word)

            url_element = article.find('a', class_='post__title_link')
            url = url_element.attrs.get('href')
            name = url_element.text

            date_element = article.find('span', class_='post__time')
            date = date_element.text
            print(f'{NL}Найдена статья, которая соответствует заданным ключевым словам: {NL}{date} - {name} - {url}')
            interesting_articles.append([date, name, url])

print(f'{NL}Cтатьи, которые соответствуют заданным словам в тексте: {len(interesting_articles)} шт. {NL}{interesting_articles}')
