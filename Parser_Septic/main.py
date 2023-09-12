import requests
import time
from bs4 import BeautifulSoup
from collections import Counter
from pprint import pprint
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from fake_useragent import UserAgent
from random import randrange


def write_google_sheets(result, normal_text):
    CREDENTIALS_FILE = '/home/tran1l/Python/Parser/Parser_Septic/septikparser-7188565d193a.json'
    spreadsheet_id = '1p0QPsmDPdg0z2duTfqjQUvjQtNjKVFm4kg_3VCvTlvY'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']
    )
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets','v4', http = httpAuth)
    values = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range = f'Лист1!B1',
        valueInputOption = "RAW",
        body = {
        "values": normal_text}
    ).execute()

    values = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range = f'Лист1!A1',
            valueInputOption = "RAW",
            body = {
            "values": result}
    ).execute()


def parser_irecommend():
    cookies = {
        'ab_var': '1',
        '_ga': 'GA1.2.917714444.1668080814',
        '_gid': 'GA1.2.928869723.1668080814',
        'stats_s_a': 'EHrvrehrrQd9rPje0Yyp%2FRpiW%2FhaZHjnLGyFId0iwBhy9IMakAA1QAIUJJmDZ1qw',
        'ss_uid': '16680808135364122',
        'stats_u_a': 'cg5ZqfeUsCd9avMj9v1UDjSg74Lz%2Bnow1k0s4DAw78KfIkYTxZ0TYlfkEHoCwRfj5fmqB%2BDNDBgQcFlY1akhqrfNh6VCLOvq',
        '_ym_uid': '166808081573164787',
        '_ym_d': '1668080815',
        'v': '45',
        '_ym_visorc': 'b',
        '_ym_isad': '1',
        'ss_hid': '28373158',
        'pmtimesig': '[[1668155639217,0],[1668155675807,36590]]',
        '_buzz_fpc': 'JTdCJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi5pcmVjb21tZW5kLnJ1JTIyJTJDJTIyZXhwaXJlcyUyMiUzQSUyMlNhdCUyQyUyMDExJTIwTm92JTIwMjAyMyUyMDA4JTNBMzglM0EyMyUyMEdNVCUyMiUyQyUyMlNhbWVTaXRlJTIyJTNBJTIyTGF4JTIyJTJDJTIydmFsdWUlMjIlM0ElMjIlN0IlNUMlMjJ2YWx1ZSU1QyUyMiUzQSU1QyUyMmQ2ZjEyMzgxMDA1OGQ3ZmM2YmM4ZDE5OWY2OTRlYTQ1JTVDJTIyJTJDJTVDJTIyZnBqc0Zvcm1hdCU1QyUyMiUzQXRydWUlN0QlMjIlN0Q=',
        'statsactivity': '14',
        'statstimer': '395',
    }

    headers = {
        'authority': 'irecommend.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'ab_var=1; _ga=GA1.2.917714444.1668080814; _gid=GA1.2.928869723.1668080814; stats_s_a=EHrvrehrrQd9rPje0Yyp%2FRpiW%2FhaZHjnLGyFId0iwBhy9IMakAA1QAIUJJmDZ1qw; ss_uid=16680808135364122; stats_u_a=cg5ZqfeUsCd9avMj9v1UDjSg74Lz%2Bnow1k0s4DAw78KfIkYTxZ0TYlfkEHoCwRfj5fmqB%2BDNDBgQcFlY1akhqrfNh6VCLOvq; _ym_uid=166808081573164787; _ym_d=1668080815; v=45; _ym_visorc=b; _ym_isad=1; ss_hid=28373158; pmtimesig=[[1668155639217,0],[1668155675807,36590]]; _buzz_fpc=JTdCJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi5pcmVjb21tZW5kLnJ1JTIyJTJDJTIyZXhwaXJlcyUyMiUzQSUyMlNhdCUyQyUyMDExJTIwTm92JTIwMjAyMyUyMDA4JTNBMzglM0EyMyUyMEdNVCUyMiUyQyUyMlNhbWVTaXRlJTIyJTNBJTIyTGF4JTIyJTJDJTIydmFsdWUlMjIlM0ElMjIlN0IlNUMlMjJ2YWx1ZSU1QyUyMiUzQSU1QyUyMmQ2ZjEyMzgxMDA1OGQ3ZmM2YmM4ZDE5OWY2OTRlYTQ1JTVDJTIyJTJDJTVDJTIyZnBqc0Zvcm1hdCU1QyUyMiUzQXRydWUlN0QlMjIlN0Q=; statsactivity=14; statstimer=395',
        'referer': 'https://irecommend.ru/catalog/list/125441-742365',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }

    for page in range(0,3):
        print(f"Страница {page}")     
        url = f'https://irecommend.ru/catalog/list/125441-742365?page={page}'
       
        response = requests.get(url=url,cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        block_url = soup.find(class_='view-content').find_all(class_='ProductTizer plate teaser-item')
        all_comment = []
        block_normal_comment = [] 

        for item in block_url:
            time.sleep(2)
            soup = BeautifulSoup(str(item), 'lxml')
            item = soup.find('a')
            item = item.get('href')
            url = 'https://irecommend.ru/'+item 
            print(url)
            response = requests.get(url=url,cookies=cookies, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            list_comments = soup.find(class_='list-comments').find_all('li', class_='item')
            for comment in list_comments:
                try:
                    time.sleep(2) 
                    soup = BeautifulSoup(str(comment), 'lxml')
                    comment = soup.find('a', class_='more')
                    comment = comment.get('href')
                    url = 'https://irecommend.ru/'+comment
                    response = requests.get(url=url,cookies=cookies, headers=headers)
                    soup = BeautifulSoup(response.text, 'lxml')
                    comment = soup.find(class_='description hasinlineimage')       
                    result_comment= []
                    normal_comment= comment.text.strip().replace('\n',' ').replace('\t',' ').strip().replace('.','\n')
                    comment = comment.text.strip().replace('\n',' ').replace('(',' ').replace(')',' ').replace('!',' ').replace(',',' ').replace('-',' ').replace('.',' ')
                    print('-----------',url)
                    minus = ''
                    plus = ''
                    try:
                        ratio_plus = soup.find(class_='plus').find_all('li')
                        ratio_minus = soup.find(class_='minus').find_all('li') 
                        normal_comment += '\nДостоинства\n'
                        for j in ratio_plus:
                            plus += j.text+' '
                        normal_comment += plus+'\n' + 'Недостатки\n'
                        for j in ratio_minus: 
                            minus += j.text+' '
                        normal_comment += minus
                    except:
                        pass
                    result_comment.append(normal_comment)
                    block_normal_comment.append(result_comment)
                    all_comment.extend((comment+' '+plus+' '+minus).split())
                     
                except:
                    print('skip')
    return all_comment, block_normal_comment
    

def parser_otzovik():
    cookies = {
        'ssid': '3111955236',
        'refreg': '1668081408~https%3A%2F%2Fwww.fl.ru%2F',
        '_ym_uid': '1668081412622950503',
        '_ym_d': '1668081412',
        '_ym_isad': '1',
        'ROBINBOBIN': '8ad8c0a9f4fb5a30ce5ce337d6',
        'guid': '2c2f5c5569062f9f1bef2264360f1eef',
    }

    headers = {
        'authority': 'otzovik.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }

    url = 'https://otzovik.com/?search_text=%D0%9A%D0%BE%D0%BC%D0%BF%D0%B0%D0%BD%D0%B8%D1%8F+%D1%81%D0%B5%D0%BF%D1%82%D0%B8%D0%BA&x=0&y=0'
    all_comment = [] 
    response = requests.get(url=url,cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    block = soup.find('tbody').find_all('tr', class_='item sortable')
    normal_text = ''
    block_normal_text = [] 
    for item in block:
        time.sleep(2)
        soup = BeautifulSoup(str(item), 'lxml')
        item = soup.find('a',class_='product-name')
        url = 'https://otzovik.com/'+item.get('href')
        response = requests.get(url=url,cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        block_comments = soup.find(class_='review-list-2 review-list-chunk').find_all(class_='review-btn review-read-link')
        for comment in block_comments:
            time.sleep(2)
            url = 'https://otzovik.com'+comment.get('href')    
            print(url)
            response = requests.get(url=url,cookies=cookies, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            plus = soup.find(class_='review-plus')
            minus = soup.find(class_='review-minus')
            comment = soup.find(class_='review-body description')
            normal_text= comment.text.strip().replace('\n',' ').replace('\t',' ').strip().replace('.','\n')
            normal_text+=f'\nДостоинсва \n{plus.text}\n'
            normal_text+=f'Недостатки \n{minus.text}\n'
            comment = comment.text.strip().replace('\n',' ').replace('(',' ').replace(')',' ').replace('!',' ').replace(',',' ').replace('-',' ').replace('.',' ')
            all_comment.extend((comment+' '+plus.text+' '+minus.text).split())
            result_block = []
            result_block.append(normal_text)
            block_normal_text.append(result_block)
    return all_comment, block_normal_text

def main():
    comments_otzovik,normal_text2 = parser_otzovik()
    comments_irecommed, normal_text = parser_irecommend()
    comments = comments_irecommed + comments_otzovik
    result = Counter(comments)
    normal_text = normal_text+normal_text2 
    ofn_result = [] 
    for key in result:
        word = []
        if int(result[key]) > 19:
            word.append(key)
            ofn_result.append(word) 
    write_google_sheets(ofn_result,normal_text)
    

if __name__ == "__main__":
    main()