import requests
from bs4 import BeautifulSoup

# CONSTANTS
KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'urllib', 'JavaScript', 'JS']
URL = 'https://habr.com/ru/all/'
NL = '\n'
is_relative = False
interesting_articles = [] #save here passed filter articles

keywords_lower = [element.lower() for element in KEYWORDS];
print('Ищем по следующим ключевым словам: ', keywords_lower)

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
    #print('***', hubs)
    for hub in hubs:
        hub_lower = hub.text.lower()
        # ищем вхождение хотя бы одного желаемого хаба

        data = []
        for key in keywords_lower:
            data.append(hub_lower in key)
        #print('***', data)


        if any(data):
            title_element = article.find('a', class_='post__title_link')
            name = title_element.text
            url = title_element.attrs.get('href')
            date_element = article.find('span', class_='post__time')
            date = date_element.text
            print(f'{NL}Найдена статья, которая соответствует заданным ключевым словам: {NL}{date} - {name} - {url}')
            interesting_articles.append([date, name, url])
        #print('***', len(interesting_articles), interesting_articles)

        # # так как пост уже нам подошел - дальше нет смысла проверять хабы
        # break

    # additional article text check
print()
for element in interesting_articles:
    result2 = requests.get(element[2])
    soup2 = BeautifulSoup(result2.text, 'html.parser')
    articles2 = soup.find_all('article', class_='post post_preview')
    intext_words = []  # save here keywords from article text
    for article in articles2:
        for word in KEYWORDS:
            if word.lower() in article.text.lower():
                is_relative = True
                intext_words.append(word)




if is_relative:
    print(f'{NL}Cтатьи, которые соответствуют заданным ключевым словам и словам в тексте: {len(interesting_articles)} шт. {NL}{interesting_articles}')
else:
    print('Не найдено статей соответствующих заданным ключевым словам и словам в тексте')
