# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import csv
from pyecharts.charts import Pie, Line, Boxplot, Funnel, Liquid, Sunburst
from pyecharts import options as opts

# 大连地区房价分布
# 近几年房价走势

city = ['北京', '天津', '保定', '廊坊']
newhouse = ['https://newhouse.fang.com/house/s/a77-b9{}/', 'https://tj.newhouse.fang.com/house/s/a77-b9{}/',
            'https://bd.newhouse.fang.com/house/s/a77-b9{}/', 'https://lf.newhouse.fang.com/house/s/a77-b9{}/']

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}


def write_to_csv(ips, city):
    with open(city + '.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerows(ips)


def run(url_, city, idx):
    print("爬取{}市, 第{}页".format(city, idx))
    url = url_.format(idx)
    html = requests.get(url, headers=header)
    soup = BeautifulSoup(html.content, 'lxml', from_encoding='gb18030')

    names = [div.a.text.strip() for div in soup.find_all('div', attrs={'class': 'nlcd_name'})]

    moneys = [re.sub(r'</?\w+[^>]*>', '', str(div)).strip() for div in
              soup.find_all('div', attrs={'class': 'nhouse_price'})]

    houses = list(zip(names, moneys))
    return houses


def pa():
    for city_idx, house_url in enumerate(newhouse):
        for page in range(1, 100 + 1):
            one_page_data = run(house_url, city[city_idx], page)
            if not one_page_data:
                break
            write_to_csv(one_page_data, city[city_idx])
            print(one_page_data)


def draw():
    count_t = {'0-300W': 0, '300W-700W': 0, '700W-1000W': 0, '1000W+': 0}
    count_m = {'0-5000m^2/s': 0, '5000-10000m^2/s': 0, '10000+m^2/s': 0}

    houses = []
    for filename in [c + '.csv' for c in city]:
        with open(filename, 'r') as f:
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

    Pie().add('按套卖', list(count_t.items())).render('t.html')
    Pie().add('按面积卖', list(count_m.items())).render('m.html')


def draw1():
    count_m = {'0-3000m^2/s': 0, '3000-5000m^2/s': 0, '5000-7000m^2/s': 0, '7000-10000m^2/s': 0, '10000+m^2/s': 0}

    houses = []
    for filename in [c + '.csv' for c in city]:
        with open(filename, 'r') as f:
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

    Line().add_xaxis(list(count_m.keys())).add_yaxis("", list(count_m.values()),
                                                     areastyle_opts=opts.AreaStyleOpts(opacity=0.5)).set_global_opts(
        title_opts=opts.TitleOpts(title="房价分布折现面积图")).render("房价分布折现面积图.html")


def draw2():
    count_m = {'0-3000m^2/s': 0, '3000-5000m^2/s': 0, '5000-7000m^2/s': 0, '7000-10000m^2/s': 0, '10000+m^2/s': 0}

    houses = []
    for filename in [c + '.csv' for c in city]:
        with open(filename, 'r') as f:
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

    Funnel().add("", list(count_m.items())).set_global_opts(title_opts=opts.TitleOpts(title="房价漏斗图")).render(
        "房价漏斗图.html")


if __name__ == '__main__':
    # pa()
    draw1()
    draw2()
