import os
import csv
import codecs

from href import get_all_song_links
from song import get_lyrics


# Функция разбивает текст песни на части, каждая из которых содержит не менее 20 слов
def words20(lines):
    song_parts = []
    current_part = ''
    for line in lines:
        if line != '':
            current_part += line + ' '

        length = len(current_part.split())
        if length >= 20:
            song_parts.append(current_part)
            current_part = ''
    if length < 11 and len(song_parts) > 0:
        song_parts[-1] = song_parts[-1] + current_part
    else:
        song_parts.append(current_part)
    return song_parts


# Функция записывает список строк в CSV-файл
def append_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow([row])

# Функция считывает строки из CSV-файла и возвращает их в виде списка
def get_from_csv(filename):
    song_links = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            song_links.append(row[0])
    return song_links

# Функция находит все пути к файлам 'urls.csv' в указанной корневой папке
def find_csv_paths(root_folder):
    csv_paths = []
    for root, dirs, files in os.walk(root_folder):
        if 'urls.csv' in files:
            csv_paths.append(os.path.join(root, 'urls.csv'))
    return csv_paths


# Основная функция, управляющая процессом получения ссылок на песни, их парсинга и сохранения
def main():
    csv_paths = find_csv_paths('songs')
    os.makedirs('songs', exist_ok=True)

    # user_input = 'https://genius.com/artists/Obladaet/songs'
    user_input = input(f'\nВведите ссылку на список песен исполнителя с genius. Как пример: \nhttps://genius.com/artists/Obladaet/songs\n\n' +
                       f'Либо путь внутри проекта. Найденные файлы с ссылками:\n' + "\n".join(csv_paths) + '\n\n>')
    
    song_links = []
    if user_input.startswith('https'):
        url = user_input
        start = url.find('artists/') + len('artists/')
        author = url[start:-5]

        print('\n------------------Получение ссылок на песни исполнителя------------------')
        song_links = get_all_song_links(url)
        # song_links = ['https://genius.com/Markul-last-ticket-lyrics']
        
        os.makedirs('songs/' + author, exist_ok=True)
        append_to_csv(song_links, 'songs/' + author + '/urls.csv')
    else:
        path = user_input
        start = path.find('songs\\\\') + len('songs\\\\')
        author = path[start:-9]
        song_links = get_from_csv(path)

    print('\n-----------------------------Ссылки получены-----------------------------\n')


    num = 0
    print('\n----------------------Парсинг песен и их сохранение----------------------\n')
    with codecs.open('songs/' + author + '/dataset.csv', 'w', 'utf-8-sig') as csvfile: 
        writer = csv.writer(csvfile)
        for song in song_links:
            num += 1
            lyrics = get_lyrics(song)
            lines = lyrics.split('\n')
            song_parts = words20(lines)
            
            for row in song_parts:
                if row != '':
                    writer.writerow(['0###' + row])
            
            print(str(num) + ' из ' + str(len(song_links)))
    print('\n-----------------------------Песни сохранены-----------------------------\n')



if __name__ == '__main__':
    main()