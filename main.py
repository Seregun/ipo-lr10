import requests  # Импортируем библиотеку requests для выполнения HTTP-запросов
from bs4 import BeautifulSoup as bs  # Импортируем BeautifulSoup из библиотеки bs4 для парсинга HTML
import json  # Импортируем библиотеку json для работы с JSON-данными

url = 'https://news.ycombinator.com/' # URL для парсинга
response = requests.get(url)  # Выполняем GET-запрос к указанному URL и сохраняем ответ в переменной response
if response.status_code != 200:  # Проверяем, успешен ли запрос (код 200 означает успех)
    print(f"Ошибка {response.status_code}")  # Если нет, выводим сообщение об ошибке
    exit()  # Завершаем выполнение программы

# Обрабатываем HTML
soup = bs(response.text, 'html.parser')
items = soup.find_all('tr', class_='athing')

# Листы для заголовков и комментариев
titles = []
comments = []

for item in items: # Получаем заголовок
    title_tag = item.select_one('span.titleline > a')
    title = title_tag.get_text(strip=True) if title_tag else "No title"
    titles.append(title)
    subtext = item.find_next_sibling('tr').find('td', class_='subtext') # Получаем количество комментариев
    if subtext:
        comments_tag = subtext.find_all('a')[-1]
        comments.append(comments_tag.get_text(strip=True).split()[0] if 'comment' in comments_tag.get_text() else '0')
    else:
        comments.append('0')
for i in range(len(titles)): # Вывод данных
    print(f"{i}. Title: {titles}; Comments: {comments};")

# Сохранение данных в data.json
data = []
for i in range(len(titles)):
    data.append({"Title": titles[i], "Comments": comments[i]})
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
# Проверка содержимого data.json
with open('data.json', 'r', encoding='utf-8') as f:
    content = json.load(f)
print(json.dumps(content, indent=4, ensure_ascii=False))

soup = bs('<!DOCTYPE html><html lang="en"></html>', 'html.parser')

# Добавление head и его содержимого
head = soup.new_tag('head')
soup.html.append(head)
meta_charset = soup.new_tag('meta', charset='UTF-8')
head.append(meta_charset)
meta_viewport = soup.new_tag('meta', attrs={'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'})
head.append(meta_viewport)

title = soup.new_tag('title')
title.string = 'Hacker News'
head.append(title)

style = soup.new_tag('style')
style.string = """
body { background: linear-gradient(135deg, #2c3e50, #ff6347); font-family: 'Times new roman', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; color: #333; }
header { background-color: rgba(0, 0, 0, 0.8); color: #fff; padding: 20px 0; text-align: center; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); }
main { padding: 20px; }
table { border-collapse: collapse; width: 90%; margin: 20px auto; background-color: rgba(255, 255, 255, 0.95); box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); border-radius: 8px; overflow: hidden; }
th, td { border: 3px solid #ddd; padding: 12px; text-align: left; }
th { background-color: #148080; color: white; }
tr:nth-child(even) { background-color: #f9f9f9; }
tr:hover { background-color: #f1f1f1; transition: background-color 0.3s; }
a { color: #fff; text-decoration: none; }
a:hover { text-decoration: underline; }
"""
head.append(style)

# Добавление body и его содержимого
body = soup.new_tag('body')
soup.html.append(body)
header = soup.new_tag('header')
h1 = soup.new_tag('h1')
h1.string = 'Hacker News'
header.append(h1)
body.append(header)
main = soup.new_tag('main')
body.append(main)
table = soup.new_tag('table')
main.append(table)
# Добавление заголовков таблицы
header_row = soup.new_tag('tr')
table.append(header_row)
headers = ['Name', 'Comments', 'Number']
for header_text in headers:
    th = soup.new_tag('th')
    th.string = header_text
    header_row.append(th)
# Добавление строк таблицы с данными
for i, item in enumerate(content, 1):
    row = soup.new_tag('tr')
    table.append(row)
    td_title = soup.new_tag('td')
    td_title.string = item['Title']
    row.append(td_title)
    td_comments = soup.new_tag('td')
    td_comments.string = item['Comments']
    row.append(td_comments)
    td_index = soup.new_tag('td')
    td_index.string = str(i)
    row.append(td_index)
# Добавление ссылки на источник данных
p = soup.new_tag('p', style='text-align: center;')
a = soup.new_tag('a', href='https://news.ycombinator.com/')
a.string = 'Источник данных'
p.append(a)
main.append(p)
with open('index.html', 'w', encoding='utf-8') as f: # сохранение в файл html
    f.write(soup.prettify())
print("Создан index.html файл")
f.close()
