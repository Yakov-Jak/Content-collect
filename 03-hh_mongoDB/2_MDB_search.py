from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
vac_db = client['vac_db']
vac_hh = vac_db.vac_hh
vac_count = 0
# salary = int(input('Введите минимальную зарплату - '))
# for vac in vac_hh.find({'$or': [{'3_min_salary': {'$gt': salary}},
#                                 {'4_max_salary': {'$gt': salary}}]}):
#     pprint(vac)
#     vac_count += 1
# print(f'Найдено {vac_count} вакансий с зарплатой больше {salary} рублей')

res = vac_hh.count_documents({'1_name': 'Chief Product Officer'})
print(res)
#
# for vac in vac_hh.find({}):
#     vac_count += 1
# print(vac_count)
