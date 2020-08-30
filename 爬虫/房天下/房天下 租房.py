# -*- coding:utf-8 -*-
import glob

import requests, threading
from bs4 import BeautifulSoup
import re, time
from pyecharts import options as opts
from pyecharts.charts import Bar3D
from tqdm import trange
from pymongo import MongoClient as Client

city = ['北京', '上海', '广东', '深圳', '沈阳', '大连']
e_city = ['beijing', 'shanghai', 'guangdong', 'shenzheng', 'shenyang', 'dalian']
eshouse = ['https://zu.fang.com/house/i3{}/', 'https://sh.zu.fang.com/house/i3{}/',
           'https://gz.zu.fang.com/house/i3{}/', 'https://sz.zu.fang.com/house/i3{}/',
           'https://sy.zu.fang.com/house/i3{}/', 'https://dl.zu.fang.com/house/i3{}/']

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/64.0.3282.186 Safari/537.36'}

is_craw = {}
proxies = []


def write_to_mongo(ips, city):
    client = Client(host='localhost', port=27017)
    db = client['zu_db']
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
    db = client['zu_db']
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
        for name in soup.find_all('dd', attrs={'class': 'info rel'}):
            names.append(name.p.a.text.strip())

        addresses = []
        for item in soup.find_all('p', attrs={'class': 'gray6 mt12'}):
            li = [i.span.text for i in item.find_all('a')]
            addresses.append("-".join(li))

        es = []
        areas = []
        for item in soup.find_all('p', attrs={'class': 'font15 mt12 bold'}):
            li = item.text.strip().split('|')
            es.append(li[1])
            areas.append(li[2])

        moneys = []
        for item in soup.find_all('p', attrs={'class': 'mt5 alingC'}):
            moneys.append(item.text)

        houses = []
        for idx in range(len(names)):
            try:
                item = [names[idx], moneys[idx], addresses[idx], areas[idx], es[idx]]
                houses.append(item)
            except Exception as e:
                print(e)

        lock.acquire()
        write_to_mongo(houses, e_city[city_id])
        lock.release()

        print("线程结束{}".format(i))


def get_real(url, pro=None):
    try:
        resp = requests.get(url, headers=header, proxies=pro, timeout=5)
        soup = BeautifulSoup(resp.content, 'html.parser', from_encoding='gb18030')
        time.sleep(1)
    except:
        return ''

    if soup.find('title').text.strip() == '跳转...':

        pattern1 = re.compile(r"var t4='(.*?)';")
        script = soup.find("script", text=pattern1)
        t4 = pattern1.search(str(script)).group(1)

        pattern1 = re.compile(r"var t3='(.*?)';")
        script = soup.find("script", text=pattern1)
        t3 = re.findall(pattern1, str(script))[-2]
        url = t4 + '?' + t3
        print(url)
        soup = get_real(url)
    elif soup.find('title').text.strip() == '访问验证-房天下':
        pass

    return soup


def craw():
    lock = threading.Lock()

    for idx in trange(len(e_city)):

        url = eshouse[idx]
        soup = get_real(url.format(2))
        try:
            page_number = int(soup.find('div', attrs={'id': 'rentid_D10_01'}).find_all('span')[-1].text[1:-1])
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
    import csv
    files = glob.glob('租房清洗后/*.csv')
    data = []
    for file in files:
        with open(file, 'r') as f:
            reader = csv.reader(f)
            c = file.split('/')[-1][3:-9]

            for item in list(reader)[1:]:
                data.append([city[e_city.index(c)], float(item[3][:-1]), float(item[5])])
    Bar3D().add(
        series_name="",
        data=data,
        xaxis3d_opts=opts.Axis3DOpts(
            name='城市',
            type_='category'
        ),
        yaxis3d_opts=opts.Axis3DOpts(
            name='单价'
        ),
        zaxis3d_opts=opts.Axis3DOpts(
            name='面积'
        )).render("bar3D.html")



if __name__ == '__main__':
    # 采集
    # craw()
    # 词云
    draw()
