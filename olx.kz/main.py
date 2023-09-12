import time
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from tkinter import *
from tkinter.ttk import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from fake_useragent import UserAgent


def get_date():
    headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"
            }
    url = 'https://www.olx.kz/d/uslugi/remont-i-stroitelstvo/'
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    val_pages = soup.find(class_='css-4mw0p4').find_all('a')
    val_pages = val_pages[-2]
    print(val_pages.text)
    for i in range(2,int(val_pages.text)):
        url = f'https://www.olx.kz/d/uslugi/remont-i-stroitelstvo/?page={i}'
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        cards = soup.find('div', class_='css-pband8').find_all('a', class_='css-rc5s2u')
        for j in cards:
            url = 'https://www.olx.kz'+j.get('href')
            selenium_code(url) 
            break
        break


def selenium_code(url):
    url = 'https://www.olx.kz/d/obyavlenie/laminat-linoleum-plintus-art-vinil-osb-dvp-ukladka-IDn8PeF.html'
    useragent = UserAgent()
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'user-agent={useragent.random}')
    options.add_argument("--disable-blink-features=AutomationControlled")
    adres = '/home/tran1l/Parsers/chromedriver'
    driver = webdriver.Chrome(executable_path=adres, options=options)
    try:
        driver.get(url=url)
        wait_element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "css-cuxnr-BaseStyles")))
        element = driver.find_element(By.CLASS_NAME, 'css-cuxnr-BaseStyles').click()
        print(element)
        time.sleep(20)
    except Exception as ex:
        print(ex) 

    finally:
        driver.close()
        driver.quit()


def main():
    get_date()

if __name__ == '__main__':
    main()