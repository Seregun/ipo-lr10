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
f =  open('data.json', 'w', encoding='utf-8')
json.dump(data, f, indent=4, ensure_ascii=False)
# Проверка содержимого data.json
f = open('data.json', 'r', encoding='utf-8')
content = json.load(f)
print(json.dumps(content, indent=4, ensure_ascii=False))
# Создание index.html
html_content = """ 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hacker News</title>
    <style>
        body {
            background: linear-gradient(135deg, #2c3e50, #3498db);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            color: #333;
        }
        header {
            background-color: rgba(0, 0, 0, 0.8);
            color: #fff;
            padding: 20px 0;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        main {
            padding: 20px;
        }
        table {
            border-collapse: collapse;
            width: 90%;
            margin: 20px auto;
            background-color: rgba(255, 255, 255, 0.95);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            overflow: hidden;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
            transition: background-color 0.3s;
        }
        a {
            color: #ff6347; /* Цвет текста ссылки */
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header>
        <h1>Hacker News</h1>
    </header>
    <main>
        <table>
            <tr>
                <th>Title</th>
                <th>Amount of Comments</th>
                <th>№</th>
            </tr>

"""
for i, item in enumerate(content, 1):
    html_content += f"<tr><td>{item['Title']}</td><td>{item['Comments']}</td><td>{i}</td></tr>\n"
html_content += """
        </table>
        <p style="text-align: center;"><a href="https://news.ycombinator.com/">Источник данных</a></p>
    </main>
</body>
</html>
"""
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
print("Создан index.html файл ")
f.close()