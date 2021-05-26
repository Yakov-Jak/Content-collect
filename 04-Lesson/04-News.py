from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient


def text_filter(my_text):
    my_text = my_text.replace("\\xa0", " ")
    my_text = my_text.replace("['", "")
    my_text = my_text.replace("']", "")
    return my_text


def make_link(link):
    if len(link) > 1:
        link = link[0]
    else:
        pass
    link = text_filter(str(link))
    if "http" in link:
        return link
    else:
        link = news_s2 + link
        return link


client = MongoClient('127.0.0.1', 27017)
news_db = client['news_db']
news_col = news_db.news_col
news_col.delete_many({})

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/90.0.4430.212 Safari/537.36'}

news_s1 = 'https://yandex.ru/news'
news_s2 = 'https://lenta.ru'
news = []
response = requests.get(news_s1)
dom = html.fromstring(response.text)
items = dom.xpath("//div[contains(@class, 'news-top-flexible-stories')]/div[contains(@class, 'mg-grid__col')]")

for item in items:
    news_i = {'name': text_filter(str(item.xpath(".//a[@class='mg-card__link']/h2[@class]/text()"))),
              'link': item.xpath(".//a[@class='mg-card__link']/@href")[0],
              'source': text_filter(str(item.xpath(".//a[@class='mg-card__source-link']/text()"))),
              'time': text_filter(str(item.xpath(".//span[@class='mg-card-source__time']/text()")))}
    news_col.insert_one(news_i)
    news.append(news_i)

response = requests.get(news_s2)
dom = html.fromstring(response.text)
items = dom.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[contains(@class, 'item')]")

for item in items:
    news_i = {'name': make_link(item.xpath(".//a/text()")).replace("https://lenta.ru", "").replace("\xa0", " "),
              'link': make_link(item.xpath(".//a/@href")),
              'source': "Лента.ру",
              'time': make_link(item.xpath(".//@datetime")).replace("https://lenta.ru ", "")}
    news.append(news_i)
    news_col.insert_one(news_i)

pprint(news)
