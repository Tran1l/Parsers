import time
# import collections import Counter
import json
import xlsxwriter
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from tkinter import *
from tkinter.ttk import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl.reader.excel import load_workbook
import pyperclip
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import csv
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime


def parser(url):
    url = 'https://www.wildberries.ru/brands/s-family'
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-blink-features=AutomationControlled")
    adres = '/home/tran1l/Parsers/pinacle/chromedriver'
    driver = webdriver.Chrome(executable_path=adres, options=options) 
    try:
        driver.get(url=url)
        element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "product-card.j-card-item.j-good-for-listing-event")))
        urls = driver.find_elements(By.CLASS_NAME, 'product-card__main.j-card-link')
    except Exception as ex:
        print(ex)
        
    parser_page(urls)


def parser_page(urls):
    schet = 0
    start_time = datetime.now()
    y_excel = 1
    x_excel =0
    title_excel = []
    workbook = xlsxwriter.Workbook('hello.xlsx') 
    worksheet = workbook.add_worksheet()  
    for url in urls:

        schet += 1 
        print(f'[INFO] Парсинг {schet}/{len(urls)} товара ')
        title_all_write = []
        all_write_name=[]
        url = url.get_attribute('href')

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-blink-features=AutomationControlled")
        adres = '/home/tran1l/Parsers/pinacle/chromedriver'
        driver = webdriver.Chrome(executable_path=adres, options=options)
        try:
            driver.get(url=url)
            element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "collapsible__toggle.j-parameters-btn.j-wba-card-item.j-wba-card-item-show")))
            price = driver.find_element(By.CLASS_NAME, 'price-block__final-price') 
            price = price.text.replace('₽', '').replace(' ','')
            categori = driver.find_element(By.CLASS_NAME, 'breadcrumbs__container')
            soup = BeautifulSoup(categori.get_attribute("innerHTML"), 'lxml')
            categori = soup.text.split()
            categor = ''
            for item in range(1, len(categori)):
                categor += categori[item] + ' '
        except Exception as ex:
            print(ex)

        url = url.split('/')
        url = url[-2]
        part = url[0:len(url)-3]
        val = url[0:len(url)-5]
        url1 = f'https://basket-0'
        url2 = f'.wb.ru/vol{val}/part{part}/{url}/info/ru/card.json'

        for item in range(1,10):
            url = url1 + f'{item}' + url2
            response = requests.get(url=url)
            soup = BeautifulSoup(response.text, 'lxml')
            try:
                title = soup.find('head').find('title')
            except:
                response = response.json()
                url_schet = response["colors"] 
                title_options = []
                options = []
                option = response["options"]
                for j in range(0,len(option)):
                    options.append(response["options"][j]["value"]) 
                    title_options.append(response["options"][j]["name"])
                
                title_all_write = ['название','артикул','цена','брeнд','категория','состав','цвет','размер','фото-ссылка'] #,'описание'
                for j in title_options:
                    title_all_write.append(j)

                    artikul = item
                    name = response["imt_name"]
                    brand = response["selling"]["brand_name"]
                    compositions = response["compositions"]
                    composition = ''
                    for j in range(0,len(compositions)):
                        composition += response["compositions"][j]["name"] + ' '
                    description = response["description"]
                    size = ''
                    sizes = response["sizes_table"]["values"]
                    for j in range(0,len(sizes)):
                        size += response["sizes_table"]["values"][j]["details"][0] + ' '
                break

        url_for_write = ''
        color = ''
        photo_urls = ''
        for i in url_schet:
            i = str(i)
            part = i[0:len(i)-3]
            val = i[0:len(i)-5]
            url1 = f'https://basket-0'
            url2 = f'.wb.ru/vol{val}/part{part}/{i}/info/ru/card.json'
            for item in range(1,10):
                url = url1 + f'{item}' + url2
                response = requests.get(url=url)
                soup = BeautifulSoup(response.text, 'lxml')
                try:
                    title = soup.find('head').find('title')
                except:
                    url_for_write += 'https://www.wildberries.ru/catalog/' + f'{i}' + '/detail.aspx?'
                    response = response.json()
   
                    color += response["nm_colors_names"] + ' | '

                    
                    for j in range(1,24):
                        req = requests.get(url='https://basket-0' +f'{item}'+ f'.wb.ru/vol{val}/part{part}/{i}/images/c246x328/{j}.jpg')
                        soup = BeautifulSoup(req.text, 'lxml')
                        try:
                            title = soup.find('head').find('title')
                            break
                        except:
                            photo_urls += 'https://basket-0' +f'{item}'+ f'.wb.ru/vol{val}/part{part}/{i}/images/c246x328/{j}.jpg' + ' | '
                            break

        
        
        all_write_name = [name, artikul, price, brand, categor, composition, color, size, photo_urls] # description,
        for j in options:
            all_write_name.append(j)
        result_write= dict(zip(title_all_write, all_write_name))
        for key in result_write:
            try:
                x_excel = title_excel.index(key)
                worksheet.write(y_excel,x_excel , result_write[key]) 
            except:
                title_excel.append(key)
                x_excel = title_excel.index(key)
                worksheet.write(0, x_excel, key)
                worksheet.write(y_excel, x_excel, result_write[key]) 
        print("Запись успешная")
        y_excel += 1
        if y_excel == 3:
            break
    workbook.close()

    driver.close()
    driver.quit()


def main(url):
    parser(url)


if __name__ == '__main__':
    # gui()
    params = ''
    main(params)