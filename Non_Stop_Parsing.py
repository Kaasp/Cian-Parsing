from selenium import webdriver
from selenium.webdriver.common.by import By
import fast_bitrix24
import time
import csv
import asyncio


def get_source_html(url):
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        time.sleep(7)
        cards = driver.find_elements(By.CLASS_NAME, '_93444fe79c--content--lXy9G')
        
        for i in cards:
            click = i.find_element(By.CLASS_NAME, '_93444fe79c--button--vynM5')
            if click.text in 'Назначить просмотр':
                continue
            else:
                click.click()
                
        for i in cards:
            try:
                link = i.find_element(By.CLASS_NAME, '_93444fe79c--link--eoxce')
                link1 = link.get_attribute('href')
            except Exception:
                continue
            
            try:    #Номер телефона
                phone = i.find_element(By.CLASS_NAME, '_93444fe79c--button--vynM5').text
                csv_file = csv.reader(open('data1.csv', "r", encoding='utf-8'), delimiter=";")
                for row in csv_file:
                    if phone[0:16] in row[-1]:
                        raise Exception
            except Exception:
                continue

            #Ссылка
            link = i.find_element(By.CLASS_NAME, '_93444fe79c--link--eoxce')
            link1 = link.get_attribute('href')

            #Параметры
            try:
                parameters = i.find_element(By.CLASS_NAME, '_93444fe79c--subtitle--vHiOV')
                parameters1 = parameters.text
            except Exception:
                parameters1 = ''

            #Адрес
            try:
                full_adress = []
                adress1 = ''
                adress = i.find_elements(By.CSS_SELECTOR, '._93444fe79c--link--NQlVc')
                for e in adress:
                    full_adress.append(e.text)
                    for a in full_adress:
                        adress1 += f'{a}, '
            except Exception:
                full_adress = []

            #Описание
            try:
                description = i.find_element(By.CSS_SELECTOR, '._93444fe79c--wrapper--LzUxV p').text
            except Exception:
                description = ''


            with open('data1.csv', 'a', encoding="utf-8", newline='') as file:
                writer = csv.writer(file)

                writer.writerow(
                    [f'{link1}; ID {link1[30:39]}; {adress1}; {parameters1}; {description}; {phone[0:16]}']
                )
                
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            tasks = {'fields': {
                      'TITLE': f'Аренда-{link1[30:38]}',
                      'CREATED_BY_ID': "79432",
                      'CURRENCY_ID': 'RUB',
                      'HAS_PHONE': 'Y',
                      'PHONE': [{"VALUE": phone[0:16].replace('-', ''), "VALUE_TYPE": "MOBILE"}],
                      'NAME': f'Аренда-{link1[30:38]}',
                      'CONTACT_ID': '',
                      'ADDRESS_2': parameters1,
                      'ADDRESS_REGION': adress1,
                      'ASSIGNED_BY_ID': "208989",
                      'COMMENTS': description,
                      'SOURCE_ID': 'UC_MJ2R11',
                      'UF_CRM_1662024810047': link1,
                      'OPENED': 'Y',
                  }}
            
            b = fast_bitrix24.Bitrix('bitrix_api_link-key')
            with b.slow():
                results = b.call('crm.lead.add', tasks)
                time.sleep(5)
    







    except Exception as _ex:
        print(_ex)
    finally:
        print('vse good')


def main():
    while True:
        time.sleep(30)
        get_source_html(
            url=f'https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&is_by_homeowner=1&offer_type=flat&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1&sort=creation_date_desc&type=4')


if __name__ == '__main__':
    main()