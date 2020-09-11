# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import csv
from pyecharts.charts import Pie, Bar
from pyecharts import options as opts

# 近几年房价走势

url = 'https://dl.newhouse.fang.com/house/s/b9{}/'

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}


def pachong():
    for page in range(1, 100 + 1):
        print("第{}页".format(page))
        url_ = url.format(page)
        html = requests.get(url_, headers=header)
        soup = BeautifulSoup(html.content, 'lxml', from_encoding='gb18030')
        names = []
        for div in soup.find_all('div', attrs={'class': 'nlcd_name'}):
            names.append(div.a.text.strip())
        if not names:
            break
        moneys = []
        for div in soup.find_all('div', attrs={'class': 'nhouse_price'}):
            moneys.append(re.sub(r'</?\w+[^>]*>', '', str(div)).strip())

        houses = list(zip(names, moneys))
        with open('data.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerows(houses)


def xianshi():
    count_t = {'0-300W': 0, '300W-700W': 0, '700W-1000W': 0, '1000W+': 0}
    count_m = {'0-5000m^2/s': 0, '5000-10000m^2/s': 0, '10000+m^2/s': 0}

    houses = []

    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[-1] != '价格待定':
                houses.append(row)

    m = list(map(lambda x: (x[0], re.findall(r'\d+\.?\d*', x[-1])[0]), filter(lambda x: x[-1].find('套') == -1, houses)))
    t = list(map(lambda x: (x[0], re.findall(r'\d+\.?\d*', x[-1])[0]), filter(lambda x: x[-1].find('套') != -1, houses)))

    # 统计按套卖
    for name, price in t:
        price = float(price)
        if price <= 300:
            count_t['0-300W'] += 1
        elif price <= 700:
            count_t['300W-700W'] += 1
        elif price <= 1000:
            count_t['700W-1000W'] += 1
        else:
            count_t['1000W+'] += 1

    # 统计按面积卖
    for name, price in m:
        price = float(price)
        if price <= 5000:
            count_m['0-5000m^2/s'] += 1
        elif price <= 10000:
            count_m['5000-10000m^2/s'] += 1
        else:
            count_m['10000+m^2/s'] += 1

    Pie().add('按套卖', list(count_t.items())).render('按套卖.html')
    Pie().add('按面积卖', list(count_m.items())).render('按面积卖.html')



def draw1():
    count_m = {'0-3000m^2/s': 0, '3000-5000m^2/s': 0 , '5000-7000m^2/s': 0, '7000-10000m^2/s': 0, '10000+m^2/s': 0}


    houses = []

    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[-1] != '价格待定':
                houses.append(row)

    m = list(map(lambda x: (x[0], re.findall(r'\d+\.?\d*', x[-1])[0]), filter(lambda x: x[-1].find('套') == -1, houses)))

    # 统计按面积卖
    for name, price in m:
        price = float(price)
        if price <= 3000:
            count_m['0-3000m^2/s'] += 1
        elif price <= 5000:
            count_m['3000-5000m^2/s'] += 1
        elif price <= 7000:
            count_m['5000-7000m^2/s'] += 1
        elif price <= 10000:
            count_m['7000-10000m^2/s'] += 1
        else:
            count_m['10000+m^2/s'] += 1
    Bar().add_xaxis(list(count_m.keys())).add_yaxis('', list(count_m.values())).render("房价分布.html")


def draw2():
    count_m = {'0-3000m^2/s': 0, '3000-5000m^2/s': 0 , '5000-7000m^2/s': 0, '7000-10000m^2/s': 0, '10000+m^2/s': 0}

    houses = []

    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[-1] != '价格待定':
                houses.append(row)

    m = list(map(lambda x: (x[0], re.findall(r'\d+\.?\d*', x[-1])[0]), filter(lambda x: x[-1].find('套') == -1, houses)))

    # 统计按面积卖
    for name, price in m:
        price = float(price)
        if price <= 3000:
            count_m['0-3000m^2/s'] += 1
        elif price <= 5000:
            count_m['3000-5000m^2/s'] += 1
        elif price <= 7000:
            count_m['5000-7000m^2/s'] += 1
        elif price <= 10000:
            count_m['7000-10000m^2/s'] += 1
        else:
            count_m['10000+m^2/s'] += 1

    Pie().add("",
              list(count_m.items()),
              radius=["30%", "75%"],
              rosetype="radius",
              label_opts=opts.LabelOpts(is_show=False),
              ).render("平米分布玫瑰图.html")


if __name__ == '__main__':
    # 采集
    # pachong()
    # xianshi()
    draw1()
    draw2()
