# -*- coding:utf-8 -*-
import requests, json, threading
from bs4 import BeautifulSoup
import re
from pyecharts.charts import Pie, Bar, Line, Scatter3D, Bar3D
from tqdm import trange
from pymongo import MongoClient as Client

import csv
from pyecharts import options as opts

city = ['北京', '上海', '广东', '深圳', '沈阳', '大连']
e_city = ['beijing', 'shanghai', 'guangdong', 'shenzheng', 'shenyang', 'dalian']
eshouse = ['https://esf.fang.com/house/i3{}/', 'https://sh.esf.fang.com/house/i3{}/',
           'https://gz.esf.fang.com/house/i3{}/', 'https://sz.esf.fang.com/house/i3{}/',
           'https://sy.esf.fang.com/house/i3{}/', 'https://dl.esf.fang.com/house/i3{}/']

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/64.0.3282.186 Safari/537.36'}

is_craw = {}


def write_to_mongo(ips, city):
    '''将数据写入mongoDB'''
    client = Client(host='localhost', port=27017)
    db = client['fs_db']
    coll = db[city + '_good']

    for ip in ips:
        coll.insert_one({'name': ip[0], \
                         'price': ip[1],
                         'addresses': ip[2],
                         'areas': ip[3],
                         'eq': ip[4]})
    client.close()


def read_from_mongo(city):
    client = Client(host='localhost', port=27017)
    db = client['fs_db']
    coll = db[city + '_good']
    li = coll.find()
    client.close()
    return li


class Consumer(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self, args=args)

    def run(self):

        global is_craw
        url_demo, i, city_id, lock = self._args
        print("{}, 第{}页".format(city[city_id], i))
        url = url_demo.format(i)

        soup = get_real(url)

        names = []
        for name in soup.select('.tit_shop'):
            names.append(name.text.strip())

        addresses = []
        for item in soup.find_all('p', attrs={'class': 'add_shop'}):
            address = item.a.text + " " + item.span.text
            addresses.append(address.replace('\t', '').replace('\n', ''))

        es = []
        for item in soup.find_all('p', attrs={'class': 'tel_shop'}):
            es.append(item.text.replace('\t', '').replace('\n', ''))

        moneys = []
        for money in soup.find_all("span", attrs={"class": 'red'}):
            moneys.append(money.text.strip())

        areas = []
        for area in soup.find_all('dd', attrs={'class': 'price_right'}):
            areas.append(area.find_all('span')[-1].text)

        houses = []
        for idx in range(len(names)):
            try:
                # item = [names[idx], moneys[idx], codes[idx], addresses[idx], areas[idx], es[idx], coms[idx]]
                item = [names[idx], moneys[idx], addresses[idx], areas[idx], es[idx]]
                houses.append(item)
            except Exception as e:
                print(e)

        lock.acquire()
        print(houses)
        write_to_mongo(houses, e_city[city_id])
        lock.release()

        print("线程结束{}".format(i))


def get_real(url):
    resp = requests.get(url, headers=header)
    soup = BeautifulSoup(resp.content, 'html.parser', from_encoding='gb18030')
    if soup.find('title').text.strip() == '跳转...':

        pattern1 = re.compile(r"var t4='(.*?)';")
        script = soup.find("script", text=pattern1)
        t4 = pattern1.search(str(script)).group(1)

        pattern1 = re.compile(r"var t3='(.*?)';")
        script = soup.find("script", text=pattern1)
        t3 = re.findall(pattern1, str(script))[-2]
        url = t4 + '?' + t3
        HTML = requests.get(url, headers=header)
        soup = BeautifulSoup(HTML.content, 'html.parser', from_encoding='gb18030')
    elif soup.find('title').text.strip() == '访问验证-房天下':
        pass

    return soup


def craw():
    lock = threading.Lock()

    for idx in trange(len(e_city)):

        url = eshouse[idx]
        soup = get_real(url.format(2))
        try:
            page_number = int(soup.find('div', attrs={'class': 'page_al'}).find_all('span')[-1].text[1:-1])
            pages = list(range(1, page_number + 1))
        except:
            pages = list(range(1, 101))
        url_demo = url

        ts = []
        while len(pages) != 0:
            for i in range(10):
                t = Consumer((url_demo, pages.pop(), idx, lock))
                t.start()
                ts.append(t)

                if len(pages) == 0:
                    break

            for t in ts:
                t.join()
                ts.remove(t)


def draw():
    areas = ['0-50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350', '350+']
    dic = {}

    with open("清洗后城市二手房数据.csv", 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        data = list(reader)
        Bar3D().add(
            series_name="",
            data=[[item[0], item[4], item[6]]for item in data],
            xaxis3d_opts=opts.Axis3DOpts(
                name='城市',
                type_='category'
            ),
            yaxis3d_opts=opts.Axis3DOpts(
                name='总价'
            ),
            zaxis3d_opts=opts.Axis3DOpts(
                name='面积'
            )).render("bar3D.html")
    #
    #     for row in list(reader)[1:]:
    #         if row[0] not in dic:
    #             dic[row[0]] = []
    #         else:
    #             dic[row[0]].append(row)
    #
    # print(list(dic.items()))

    #         if row[0] not in dic:
    #             dic[row[0]] = {'price':{}, 'area':{}}
    #         else:
    #             area = float(row[6])
    #             price = float(row[4])
    #             if area < 50:
    #                 q = '0-50'
    #             elif area < 100:
    #                 q = '50-100'
    #             elif area < 150:
    #                 q = '100-150'
    #             elif area < 200:
    #                 q = '150-200'
    #             elif area < 250:
    #                 q = '200-250'
    #             elif area < 300:
    #                 q = '250-300'
    #             elif area < 350:
    #                 q = '300-350'
    #             else:
    #                 q = '350+'
    #
    #             if q not in dic[row[0]]['area']:
    #                 dic[row[0]]['area'][q] = 0
    #             else:
    #                 dic[row[0]]['area'][q] += 1
    #
    #             if price < 50:
    #                 q = '0-50'
    #             elif price < 100:
    #                 q = '50-100'
    #             elif price < 150:
    #                 q = '100-150'
    #             elif price < 200:
    #                 q = '150-200'
    #             elif price < 250:
    #                 q = '200-250'
    #             elif price < 300:
    #                 q = '250-300'
    #             elif price < 350:
    #                 q = '300-350'
    #             else:
    #                 q = '350+'
    #
    #             if q not in dic[row[0]]['price']:
    #                 dic[row[0]]['price'][q] = 0
    #             else:
    #                 dic[row[0]]['price'][q] += 1
    #
    # data = []
    # for key1 in dic:
    #         for key3 in areas:
    #             if key3 in dic[key1]['price']:
    #                 price = dic[key1]['price'][key3]
    #                 for key3 in areas:
    #                     if key3 in dic[key1]['area']:
    #                         area = dic[key1]['area'][key3]
    #                         data.append([key1, price, area])
    #
    # Scatter3D().add(
    #     series_name="",
    #     data=data,
    #     xaxis3d_opts=opts.Axis3DOpts(
    #         name='城市',
    #         type_='category'
    #     ),
    #     yaxis3d_opts=opts.Axis3DOpts(
    #         name='单价',
    #         textstyle_opts=opts.TextStyleOpts(color="#000"),
    #     ),
    #     zaxis3d_opts=opts.Axis3DOpts(
    #         name='面积'
    #     )).render("bar3D.html")


if __name__ == '__main__':
    # 采集的函数
    # craw()

    # 词云的函数
    draw()
