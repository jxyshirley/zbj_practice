from bs4 import BeautifulSoup
import requests
import time
import pymongo
import string
from pandas import read_csv

client=pymongo.MongoClient('localhost',27017)
zbj=client['zbj']
#appkaifaaa_info_list = zbj['appkaifaaa_info_list']
#itfangan_info_list = zbj['itfangan_info_list']
#rikaifa_info_list = zbj['rikaifa_info_list']##企业管理软件
##wzkf_info_list = zbj['wzkf_info_list']
#rjkf_info_list = zbj['rjkf_info_list']
#uisj_info_list = zbj['uisj_info_list']
#yxjssj_info_list = zbj['yxjssj_info_list']
#wxptkf_info_list = zbj['wxptkf_info_list']
#yidongui_info_list = zbj['yidongui_info_list']
youxikf_info_list = zbj['youxikf_info_list']
cuowu_url_list=zbj['cuowu_url_list']
##channel = 'http://shop.zbj.com/347812/'
#channel = 'http://shop.zbj.com/15647987/'
def get_item_info(channel):
    url = '{}{}'.format(channel,'evaluation.html')
    time.sleep(1)
    print(url)
    web_data= requests.get(url)
    #print(web_data)
    soup = BeautifulSoup(web_data.text,'lxml')

    ##店铺等级爬取
    shop_level_src = soup.find('img',{"align":{"absmiddle"}})
    if shop_level_src == None:
        shop_level = 0
    else:
        shop_level_src1 = shop_level_src.get('src').split('/')
        shop_level=shop_level_src1[-1].split('.')[0].split('-')[-1]
    print(shop_level)

    ##店铺评分爬取
    zbj_evaluation = soup.find('div',{"class":{"shop-evaluate-det"}})#.text
    if zbj_evaluation == None:
        zbj_evaluation_zhiliang = 0
        zbj_evaluation_sudu = 0
        zbj_evaluation_taidu = 0
    else:
        print(zbj_evaluation)
        zbj_evaluation1=zbj_evaluation.text.split('|')
        zbj_evaluation_zhiliang=zbj_evaluation1[0].split('：')[1].strip()
        zbj_evaluation_sudu = zbj_evaluation1[1].split('：')[1].strip()
        zbj_evaluation_taidu = zbj_evaluation1[2].split('：')[1].strip()
    print(zbj_evaluation_zhiliang,zbj_evaluation_sudu,zbj_evaluation_taidu)

    ##店铺经营状况抓取
    zbj_business = soup.find('div', {"class": {"personal-shop-balance"}}).text
    zbj_business1=zbj_business.split('元')
    zbj_business_incom=zbj_business1[0].split('：')[1].strip()
    zbj_business_num=zbj_business1[1].split('笔')[0].strip()
    print(zbj_business_incom,zbj_business_num)

    ##用户评价概览(全部)
    online_evaluation = soup.find('div', {"class": {"filter-comment J-filter-comment"}}).text.split(')')
    online_evaluation_haoping = online_evaluation[0].split('(')[-1]
    online_evaluation_zhongping = online_evaluation[1].split('(')[-1]
    online_evaluation_chaping = online_evaluation[2].split('(')[-1]
    print(online_evaluation_haoping,online_evaluation_zhongping,online_evaluation_chaping)

    ##用户评价概览(分时期）
    online_evaluation_1 = soup.find('div', {"class": {"shop-comment-bd"}})
    online_evaluation_11=str(online_evaluation_1).split('</span>')[3:]
    ##最近一周
    online_evaluation_1_1_1=online_evaluation_11[0].split('shop-com-num">')[-1]
    online_evaluation_1_1_2 = online_evaluation_11[1].split('shop-com-num">')[-1]
    online_evaluation_1_1_3 = online_evaluation_11[2].split('shop-com-num">')[-1]
    ##最近一个月
    online_evaluation_1_2_1 = online_evaluation_11[3].split('shop-com-num">')[-1]
    online_evaluation_1_2_2 = online_evaluation_11[4].split('shop-com-num">')[-1]
    online_evaluation_1_2_3 = online_evaluation_11[5].split('shop-com-num">')[-1]
    ##最近半年
    online_evaluation_1_3_1 = online_evaluation_11[6].split('shop-com-num">')[-1]
    online_evaluation_1_3_2 = online_evaluation_11[7].split('shop-com-num">')[-1]
    online_evaluation_1_3_3 = online_evaluation_11[8].split('shop-com-num">')[-1]
    ##半年以前
    online_evaluation_1_4_1 = online_evaluation_11[9].split('shop-com-num">')[-1]
    online_evaluation_1_4_2 = online_evaluation_11[10].split('shop-com-num">')[-1]
    online_evaluation_1_4_3 = online_evaluation_11[11].split('shop-com-num">')[-1]
    print(online_evaluation_1_1_1,online_evaluation_1_1_2,online_evaluation_1_1_3,online_evaluation_1_2_1,
          online_evaluation_1_2_2,online_evaluation_1_2_3,online_evaluation_1_3_1,online_evaluation_1_3_2,
          online_evaluation_1_3_3,online_evaluation_1_4_1,online_evaluation_1_4_2,online_evaluation_1_4_3)

    ##用户推荐（半年以内）
    online_recommend = soup.find('div', {"class": {"shop-comment-r"}})
    online_recommend1=str(online_recommend).split('</span>')[3:]
    online_recommend_1=online_recommend1[0].split('shop-com-num">')[-1]
    online_recommend_2 = online_recommend1[1].split('shop-com-num">')[-1]
    online_recommend_3 = online_recommend1[2].split('shop-com-num">')[-1]
    print(online_recommend_1,online_recommend_2,online_recommend_3)

    ##用户评价标签
    online_label = soup.find('ul', {"class": {"employer-impression-lists"}})
    online_label1 = str(online_label).split('</span>')
    #print(online_label1)
    i=0
    label_dict = dict()
    while i<len(online_label1)-1:
        online_label_a=online_label1[i].split('<span class="number">')
        online_label_b = online_label_a[0].split('">')[-1].strip()
        online_label_c = online_label_a[1]
        item={online_label_b:online_label_c}
        label_dict.update(item)
        i=i+1
    print(label_dict)
    #print(BeautifulSoup(online_tabel1[0],'lxml').select('li').get('title'))

    ##店铺热度爬取
    url_1 = '{}{}'.format(channel, 'salerinfo.html')
    print(url_1)
    web_data_1 = requests.get(url_1)
    soup_1 = BeautifulSoup(web_data_1.text, 'lxml')
    hot= soup_1.select('div.my-home > p > b')
    print(hot)
    day_page_view =str(str(hot[0]).split('</')[0]).split('b>')[1]
    week_page_view = str(str(hot[1]).split('</')[0]).split('b>')[1]
    collection = str(str(hot[2]).split('</')[0]).split('b>')[1]
    print(day_page_view,week_page_view,collection)

    youxikf_info_list.insert_one({'url':channel, 'shop_level': shop_level,
                                     'zhiliang': zbj_evaluation_zhiliang,'sudu': zbj_evaluation_sudu,'taidu': zbj_evaluation_taidu,
                                     'business_incom':zbj_business_incom , 'business_num': zbj_business_num,
                                     'haoping':online_evaluation_haoping, 'zhongping': online_evaluation_zhongping,'chaping': online_evaluation_chaping,
                                     'evaluation_zhou_h': online_evaluation_1_1_1,'evaluation_zhou_z': online_evaluation_1_1_2,'evaluation_zhou_c': online_evaluation_1_1_3,
                                     'evaluation_yue_h': online_evaluation_1_2_1,'evaluation_yue_z': online_evaluation_1_2_3,'evaluation_yue_c': online_evaluation_1_2_3,
                                     'evaluation_bn_h': online_evaluation_1_3_1,'evaluation_bn_z': online_evaluation_1_3_2,'evaluation_bn_c': online_evaluation_1_3_3,
                                     'evaluation_old_h': online_evaluation_1_4_1,'evaluation_old_z': online_evaluation_1_4_2,'evaluation_old_c': online_evaluation_1_4_3,
                                     'online_recommend_1':online_recommend_1,'online_recommend_2': online_recommend_2, 'online_recommend_3': online_recommend_3,
                                     'review_label': label_dict,
                                     'day_page_view': day_page_view, 'week_page_view':week_page_view,'collection': collection})
def get_url_file():
    pass

def get_channel():
    #url_file = read_csv('D://code//zbj//data//appkaifaaa_url_list.csv')

    url_file = read_csv('D://code//zbj//data//youxikf_url_list.csv')
    n=url_file.url.size
    print(n)
    k=0

    while k<n:
        channel=url_file.ix[k]['url']
        try:
            get_item_info(channel)
            k=k+1
            print(channel)
            print(k)
        except:
            cuowu_url_list.insert_one({'url':channel})
            k=k+1


get_channel()
#get_item_info(channel)

