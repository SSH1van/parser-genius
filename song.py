import re
import requests
from bs4 import BeautifulSoup


def remove_bracketed_sections(text):
    # Удаляет все текстовые секции, заключенные в квадратные скобки, из текста.
    text = re.sub(r'\[.*?\]', '', text)
    # Создает таблицу перевода для замены определенных символов
    translation_table = str.maketrans({';': '', '"': '', ' ': ' '})
    # Применяет таблицу перевода к тексту, заменяя указанные символы на пробелы.
    return text.translate(translation_table)


def get_lyrics(url):
    # Заголовки для HTTP-запроса
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Получение HTML-страницы
    response = requests.get(url, headers=headers)

    # Если запрос был успешным (код состояния 200).
    if response.status_code == 200:
        # Создание объекта BeautifulSoup для парсинга HTML-контента
        soup = BeautifulSoup(response.content, 'html.parser')

        # Нахождение всех контейнеров с текстами песен по определенному атрибуту
        lyrics_containers = soup.find_all('div', {'data-lyrics-container': 'true'})
        
        lyrics = [] # Список для хранения текста песен

        # Проход по всем найденным контейнерам с текстами песен
        for container in lyrics_containers:
            for element in container.children:
                # Если элемент является тегом <a>, <i> или <b>, добавляет его внутренние элементы в список lyrics
                if element.name == 'a' or element.name == 'i' or element.name == 'b':
                    for inner_element in element.children:
                        lyrics.append(inner_element)

                # Если элемент является строкой, добавляет его в список lyrics
                elif isinstance(element, str):
                    lyrics.append(element)
                
                # Если элемент является тегом <br>, добавляет символ новой строки в список lyrics
                elif element.name == 'br':
                    lyrics.append('\n')
            
            # Добавляет символ новой строки после каждого контейнера
            lyrics.append('\n')

        # Переменная для проверки необходимости дальнейшей обработки
        check = True
        new_lyrics = []

        # Повторная обработка списка lyrics до тех пор, пока не останется необработанных элементов
        while check:
            check = False
            for element in lyrics:
                # Если элемент является символом новой строки, добавляет его в new_lyrics
                if element == '\n':
                    new_lyrics.append('\n')
                
                # Если элемент является строкой, добавляет его в new_lyrics
                elif isinstance(element, str):
                    new_lyrics.append(element)

                # Если элемент является тегом <a>, <i>, <b> или <span>, добавляет его внутренние элементы в new_lyrics
                elif element.name == 'a' or element.name == 'i' or element.name == 'b' or element.name == 'span':
                    for inner_element in element.children:
                        new_lyrics.append(inner_element)
                    check = True

                # Если элемент является тегом <br>, добавляет символ новой строки в new_lyrics и отмечает необходимость дальнейшей обработки
                elif element.name == 'br':
                    new_lyrics.append('\n')
                    check = True

            # Обновляет список lyrics и очищает new_lyrics для следующей итерации
            lyrics[:] = new_lyrics
            new_lyrics = []
            
        # Объединяет все элементы списка lyrics в строку и удаляет лишние пробелы по краям
        text_lyrics = ''.join(lyrics).strip()
        # Удаляет текстовые секции в квадратных скобках и указанные символы
        cleaned_text_lyrics = remove_bracketed_sections(text_lyrics)
        # Возвращает очищенный текст песен
        return cleaned_text_lyrics