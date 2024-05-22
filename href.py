import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_all_song_links(url):
    # Настройка опций браузера
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Инициализация веб-драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

    # Прокрутка страницы вниз для подгрузки всех песен
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Задержка для подгрузки контента
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Парсинг ссылок на песни
    song_links = []
    list_items = driver.find_elements(By.CSS_SELECTOR, 'li.ListItem__Container-sc-122yj9e-0')
    for item in list_items:
        a_tag = item.find_element(By.CSS_SELECTOR, 'a.ListItem__Link-sc-122yj9e-1')
        if a_tag:
            song_links.append(a_tag.get_attribute('href'))

    driver.quit()
    return song_links