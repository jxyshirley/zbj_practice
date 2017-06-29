# -*- coding: utf-8 -*-
import requests
import pymongo
from bs4 import BeautifulSoup

client = pymongo.MongoClient('localhost', 27017)
zbj = client['zbj']
yxjssj_url_list = zbj['yxjssj_url_list']  # 游戏美术


def get_channel_urls(url):
    wb_data = requests.get(url)
    print(wb_data)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    links = soup.select('a.witkey-item-name')
    for link in links:
        shop_url = link.get('href')
        yxjssj_url_list.insert_one({'url': shop_url})


def start_url():
    for i in range(1, 5):
        url = 'http://www.zbj.com/yxjssj/pp{}.html'.format(i)
        print(url)
        get_channel_urls(url)


if __name__ == '__main__':
    start_url()
