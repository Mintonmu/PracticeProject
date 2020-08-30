# -*- coding:utf-8 -*-
import requests, json, threading
from bs4 import BeautifulSoup
import numpy as np
import re

from pyecharts.charts import Pie, Bar, Line, Scatter3D
from pyecharts.faker import Faker
from tqdm import trange
from pymongo import MongoClient as Client

city = ['北京', '上海', '广东', '深圳', '沈阳', '大连']
e_city = ['beijing', 'shanghai', 'guangdong', 'shenzheng', 'shenyang', 'dalian']
newhouse = ['https://newhouse.fang.com/house/s/b9{}-c9y/', 'https://sh.newhouse.fang.com/house/s/b9{}-c9y/',
            'https://gz.newhouse.fang.com/house/s/b9{}-c9y/', 'https://sz.newhouse.fang.com/house/s/b9{}-c9y/',
            'https://sy.newhouse.fang.com/house/s/b9{}-c9y/', 'https://dl.newhouse.fang.com/house/s/b9{}-c9y/']

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/64.0.3282.186 Safari/537.36'}

is_craw = {}


def write_to_mongo(ips, city):
    '''将数据写入mongoDB'''
    client = Client(host='localhost', port=27017)
    db = client['xf_db']
    coll = db[city + '_good']

    for ip in ips:
        coll.insert_one({'name': ip[0], \
                         'price': ip[1],
                         'codes': ip[2],
                         'addresses': ip[3],
                         'areas': ip[4],
                         'eq': ip[5],
                         'comment': ip[6]})
    client.close()


def read_from_mongo(city):
    client = Client(host='localhost', port=27017)
    db = client['xf_db']
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

        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser', from_encoding='gb18030')

        names = []
        for name in soup.select('.list_title_'):
            names.append(name.text)

        es = []
        addresses = []
        for item in soup.find_all('div', attrs={'class': 'c_333_f14'}):
            address = item.find_all('p')[1]
            address = address.span.text + " " + address.find('span', attrs={'class': 'iconAdress'}).attrs['title']
            addresses.append(address)
            es.append(item.p.text.replace('\t', '').replace(' ', '').replace('\r\n', ''))

        moneys = []
        for money in soup.find_all("span", attrs={"class": 'price_xf'}):
            moneys.append(money.text)

        areas = []
        for area in soup.find_all('div', attrs={'class': 'mt8'}):
            areas.append(area.p.text)

        coms = []
        codes = []

        lock.acquire()
        try:
            for a in soup.find_all('a', attrs={'class': 'list_title_'}):
                url = "https:" + a.attrs['href']
                d = url.split('.')[0].split('//')[1]
                dianpingNewcode, comment = self.get_comment(city[city_id], d)
                codes.append(dianpingNewcode)
                coms.append(comment)
        except:
            pass
        finally:
            lock.release()

        houses = []
        for idx in range(len(names)):
            try:
                item = [names[idx], moneys[idx], codes[idx], addresses[idx], areas[idx], es[idx], coms[idx]]
                houses.append(item)
            except:
                pass

        lock.acquire()
        write_to_mongo(houses, e_city[city_id])
        lock.release()

        print("线程结束{}".format(i))

    def get_comment(self, city, d):

        if d in is_craw:
            return is_craw[d], []

        url1 = "https://" + d + ".fang.com/dianping/"
        html1 = requests.get(url1, headers=header)

        soup1 = BeautifulSoup(html1.content, 'html.parser', from_encoding='gb18030')
        dianpingNewcode = soup1.find('link', attrs={'rel': 'alternate'}).attrs['href'].split('/')[-2]

        is_craw[d] = dianpingNewcode

        resp = requests.post("https://" + d + ".fang.com/house/ajaxrequest/dianpingList_201501.php", \
                             headers=header,
                             data={'city': city, 'dianpingNewcode': str(dianpingNewcode), 'pagesize': '10000',
                                   'page': '1'})

        comments = json.loads(resp.text)

        return dianpingNewcode, list(map(lambda x: x['content'], comments['list']))


def craw():
    lock = threading.Lock()

    for idx in trange(len(newhouse)):

        url = newhouse[idx]
        HTML = requests.get(url.format(1), headers=header)
        SOUP = BeautifulSoup(HTML.content, 'html.parser', from_encoding='gb18030')
        last_page = SOUP.select('.last')
        try:
            page_number = int(last_page[0]['href'].split('/')[3][2:-4])  # 根据尾页划分页码
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
    datas = []
    import csv
    with open('guangdong_清洗后-新房.csv', 'r') as f:
        data = csv.reader(f)
        pat = re.compile('\d室\d厅')
        for item in list(data)[1:]:
            if pat.match(item[5]):
                p = float(item[-1])
                m = float(item[2][:-1])

                eq = re.search(pat, item[5]).group()
                datas.append([eq, p, m])

        from pyecharts import options as opts
        (
            Scatter3D()
                .add(
                series_name="",
                data=datas,
                xaxis3d_opts=opts.Axis3DOpts(
                    name='配置',
                    type_='category'
                ),
                yaxis3d_opts=opts.Axis3DOpts(
                    name='价格',
                ),
                zaxis3d_opts=opts.Axis3DOpts(
                    name='面积',
                ),
            )
                .render("scatter3d.html")
        )


if __name__ == '__main__':
    # 采集
    # craw()
    draw()
