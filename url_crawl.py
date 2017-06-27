from bs4 import BeautifulSoup
import requests
import pymongo

client=pymongo.MongoClient('localhost',27017)
zbj=client['zbj']
#rikaifa_url_list = zbj['rikaifa_url_list']##企业管理软件
#rjkf_url_list = zbj['rjkf_url_list']##软件开发
#uisj_url_list = zbj['uisj_url_list']##UI设计
#yidongui_url_list = zbj['yidongui_url_list']##移动UI设计
#appkaifaaa_url_list = zbj['appkaifaaa_url_list']##移动APP开发
#wxptkf_url_list = zbj['wxptkf_url_list']##微信开发
#itfangan_url_list = zbj['itfangan_url_list']##IT解决方案
#wzkf_url_list = zbj['wzkf_url_list']##网站建设（网站开发）
#youxikf_url_list = zbj['youxikf_url_list']##游戏开发9页
yxjssj_url_list = zbj['yxjssj_url_list']##游戏美术



def get_channel_urls(url):
    wb_data = requests.get(url)
    print(wb_data)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    links = soup.select('a.witkey-item-name')
    for link in links:
        page_url=link.get('href')
        yxjssj_url_list.insert_one({'url': page_url})

def start_url():
    i=1
    while i<5:
        start_url='{}{}.html'.format('http://www.zbj.com/yxjssj/pp',str(i))
        print(start_url)
        get_channel_urls(start_url)
        i=i+1

start_url()


