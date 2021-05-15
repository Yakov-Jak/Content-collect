import requests
from pprint import pprint
import json

url = 'https://api.github.com/users/Yakov-Jak/repos' # смотрим пользователя Yakov-Jak - собственный реп

response = requests.get(url)
j_data = response.json()
repos = {}
# pprint(type(response))
#print(f'Репозитории {len(j_data)}')
el = 0
for i in j_data:
    repos[el] = i['name']
    el += 1
print(repos)
with open('Repos_list.json', 'w') as j_rep:
    json.dump(repos, j_rep)
