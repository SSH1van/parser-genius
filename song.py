import requests
from bs4 import BeautifulSoup
import re

def remove_bracketed_sections(text):
    text = re.sub(r'\[.*?\]', '', text)

    translation_table = str.maketrans('', '', ';" ')
    return text.translate(translation_table)


def get_lyrics(url):
    # Заголовки для HTTP-запроса
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Получение HTML-страницы
    response = requests.get(url, headers=headers)

    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        lyrics_containers = soup.find_all('div', {'data-lyrics-container': 'true'})
        
        lyrics = [] 

        for container in lyrics_containers:
            for element in container.children:
                if element.name == 'a' or element.name == 'i' or element.name == 'b':
                    for inner_element in element.children:
                        lyrics.append(inner_element)
                
                elif isinstance(element, str):
                    lyrics.append(element)
                
                elif element.name == 'br':
                    lyrics.append('\n')
               
            lyrics.append('\n')


        check = True
        new_lyrics = []
        while check:
            check = False
            for element in lyrics:
                if element == '\n':
                    new_lyrics.append('\n')
                
                elif isinstance(element, str):
                    new_lyrics.append(element)

                elif element.name == 'a' or element.name == 'i' or element.name == 'b' or element.name == 'span':
                    for inner_element in element.children:
                        new_lyrics.append(inner_element)
                    check = True
                
                elif element.name == 'br':
                    new_lyrics.append('\n')
                    check = True

            lyrics[:] = new_lyrics
            new_lyrics = []
            

        text_lyrics = ''.join(lyrics).strip()
        cleaned_text_lyrics = remove_bracketed_sections(text_lyrics)
        return cleaned_text_lyrics