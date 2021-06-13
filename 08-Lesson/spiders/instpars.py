# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from instapars.items import InstaparsItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from instapars import psw

class InstparsSpider(scrapy.Spider):
    name = 'instpars'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'Ivan_Uralov_Chel'
    insta_pwd = psw.psw()
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_users = ['toyotarussia', 'audirussia', 'mbrussia']      #Пользователь, у которого собираем посты. Можно указать список

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    posts_hash = '7ea6ae3cf6fb05e73fcbe1732b1d2a42'     #hash для получения данных по постах с главной страницы

    def parse(self, response:HtmlResponse):             #Первый запрос на стартовую страницу
        csrf_token = self.fetch_csrf_token(response.text)   #csrf token забираем из html
        yield scrapy.FormRequest(                   #заполняем форму для авторизации
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username':self.insta_login, 'enc_password':self.insta_pwd},
            headers={'X-CSRFToken':csrf_token}
        )

    def user_parse(self, response:HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:                 #Проверяем ответ после авторизации
            for el in self.parse_users:
                yield response.follow(                  #Переходим на желаемую страницу пользователя. Сделать цикл для кол-ва пользователей больше 2-ух
                    f'/{el}',
                    callback= self.user_data_parse,
                    cb_kwargs={'username':el}
            )

    # def subscribers_parse(self, response:HtmlResponse, username):
    #     print()
    #     user_id = self.fetch_user_id(response.text, username)
    #     url = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?count=12&search_surface=follow_list_page'
    #     yield response.follow(
    #         url,
    #         callback=self.subscribers_parse_next,
    #         headers={'User-Agent': 'Instagram 64.0.0.14.96'},
    #         cb_kwargs={'username':username,
    #                    'user_id':user_id,}
    #     )


    def user_data_parse(self, response:HtmlResponse, username):
        print()

        user_id = self.fetch_user_id(response.text, username)       #Получаем id пользователя
        variables={'id':user_id,                                    #Формируем словарь для передачи даных в запрос
                   'first':12}                                      #12 постов. Можно больше (макс. 50)
        url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'    #Формируем ссылку для получения данных о постах
        yield response.follow(
            url_posts,
            callback=self.user_posts_parse,
            cb_kwargs={'username':username,
                       'user_id':user_id,
                       'variables':deepcopy(variables)}         #variables ч/з deepcopy во избежание гонок
        )

    def user_posts_parse(self, response:HtmlResponse,username,user_id,variables):   #Принимаем ответ. Не забываем про параметры от cb_kwargs
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):                                          #Если есть следующая страница
            variables['after'] = page_info['end_cursor']                            #Новый параметр для перехода на след. страницу
            url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback=self.user_posts_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')     #Сами посты
        for post in posts:                                                                      #Перебираем посты, собираем данные
            item = InstaparsItem(
                user_id=user_id,
                username=username,
                photo=post['node']['display_url'],
                likes=post['node']['edge_media_preview_like']['count'],
                post=post['node']
            )
        yield item                  #В пайплайн


    #Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')


    #Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')