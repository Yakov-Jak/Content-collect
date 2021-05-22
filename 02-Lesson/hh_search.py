from bs4 import BeautifulSoup as bs
import requests
import csv
from pprint import pprint

# https://hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text=Lean&showClusters=false&customDomain=1&page=1
def sal_chek (sal_code):        #Функция проверки наличия зарплаты.
    if sal_code is None:        #Возвращает None если нет зарплаты.
        return None
    else:                       #Если зарплата есть - преобразует тег в текст и совершает предобработку в список.
        sal_code = (sal_code.getText().replace("\u202f", "")).split(' ')
        return sal_code

def sal_def (sal_text):         # Функция структурирует зарплату от\до\диапазон
    if sal_text[0].isdigit():
        sal_param = [sal_text[0], sal_text[2], sal_text[3]]
        return sal_param
    elif sal_text[0] == 'от':
        sal_param = [sal_text[1], None, sal_text[2]]
        return sal_param
    elif sal_text[0] == 'до':
        sal_param = [None, sal_text[1], sal_text[2]]
        return sal_param
    else:
        return None


search_text = 'Lean' # Поиск вакансий по запросу Lean
url = 'https://hh.ru'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
page = 0
vacancies = []

while True:
    params = {'L_save_area':'true',
              'clusters':'true',
              'enable_snippets':'true',
              'text':search_text,
              'showClusters':'false',
              'customDomain':'1',
              'page':page
              }

    response = requests.get(url+'/search/vacancy',params=params, headers=headers)
    dom = bs(response.text,'html.parser')
    vacancy_list = dom.find_all('div',{'class':'vacancy-serp-item'})
    if len(vacancy_list) == 0:
        break
    else:
        page += 1
        for vac_item in vacancy_list:
            vac_info = {}
            vac_name = vac_item.find('a').getText()
            vac_link = vac_item.find('a', {'class':'bloko-link'})['href']
            vac_salary = vac_item.find('span', {'data-qa':'vacancy-serp__vacancy-compensation'})
            vac_salary = sal_chek(vac_salary)

            if vac_salary is None:
                vac_sal_min = None
                vac_sal_max = None
                vac_sal_cur = None
            else:
                vac_salary = sal_def(vac_salary)
                vac_sal_min = vac_salary[0]
                vac_sal_max = vac_salary[1]
                vac_sal_cur = vac_salary[2]

            vac_info['1_name'] = vac_name
            vac_info['2_link'] = vac_link
            vac_info['3_min_salary'] = vac_sal_min
            vac_info['4_max_salary'] = vac_sal_max
            vac_info['5_salary_cur'] = vac_sal_cur
            vac_info['6_site'] = url
            vacancies.append(vac_info)

pprint(vacancies)
print(f'Количество вакансий собранных вакансий - {len(vacancies)}')

with open('Vac.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=vacancies[0])
    writer.writeheader()
    writer.writerows(vacancies)