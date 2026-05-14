import os
import requests
from bs4 import BeautifulSoup

# Получает HTML-содержимое главной страницы Lenta.ru
def get_lenta_news(url="https://lenta.ru"):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None

# Парсит заголовки новостей из HTML-кода
def parse_titles(html):
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    classes = ["card-mini__title", "card-big__title", "card-container__title"]
    items = soup.find_all(["span", "h3"], class_=classes)

    if not items:
        items = soup.select('span[class*="title"]')

    titles = []
    for item in items:
        text = item.get_text(strip=True)
        if text and text not in titles:
            titles.append(text)

    return titles[:10]

# Сохраняет список заголовков в текстовый файл
def save_to_local_folder(titles, filename="news.txt"):

    if not titles:
        print("Нет данных для сохранения.")
        return False

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for i, title in enumerate(titles, 1):
                f.write(f"{i}. {title}\n")
        print(f"Файл сохранен здесь: {file_path}")
        return True
    except IOError as e:
        print(f"Ошибка записи: {e}")
        return False


if __name__ == "__main__":
    html_content = get_lenta_news()
    news_titles = parse_titles(html_content)
    print(f"Найдено новостей: {len(news_titles)}")

    if save_to_local_folder(news_titles):
        print("Успешно!")
    else:
        print("Ошибка при сохранении.")