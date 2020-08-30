import pandas as pd
import requests, csv
from bs4 import BeautifulSoup
from pyecharts.charts import *

url_demo = 'https://www.lagou.com/zhaopin/{}/{}/?labelWords=label'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}


# 获取技术类别
def get_type():
    url = 'https://www.lagou.com/'

    r = requests.get(url, headers=header)

    soup = BeautifulSoup(r.text, 'lxml')

    divs = soup.find('div', attrs={'class': 'menu_box'})
    type = set()
    if divs:
        list_a = divs.find_all('a')

        for item in list_a:
            t = item.h3.text
            type.add(t.replace('#', '%23'))
    else:
        print("未找到type")
        exit(0)
    return list(type)


# 获取所有城市
def get_city():
    url = 'https://www.lagou.com/jobs/allCity.html'
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'lxml')
    uls = soup.find_all('ul', attrs={'class': 'city_list'})
    citys = []
    for ul in uls:
        lis = ul.find_all('li')
        for li in lis:
            citys.append(li.a.text)
    return citys


def read_from_csv():
    with open('data.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        data = []
        for item in reader:
            if item:
                data.append(item)
    return data


def write_to_csv(data):
    with open('data.csv', 'a', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def get_info_by_type(type, city, page, deep=0):
    deep += 1
    url = url_demo.format(type, page) + '&city=' + city
    print(url)
    r = requests.get(url, headers=header)
    # time.sleep(1)
    soup = BeautifulSoup(r.text, 'lxml')

    if soup.find('img', attrs={'alt': '404'}):
        print("404")
        return []

    lis = soup.find_all('li', attrs={'class': 'con_list_item'})
    data = []
    for li in lis:
        salary = li.attrs['data-salary']
        company = li.attrs['data-company']
        positionname = li.attrs['data-positionname']
        companyid = li.attrs['data-companyid']
        format_time = li.find('span', attrs={'class': 'format-time'}).text
        info = li.find('div', attrs={'class': 'p_bot'}).div.text
        ifs = info.split('/')
        xl = '大专'
        if len(ifs) == 2:
            xl = ifs[-1].strip()
        in_data = [city, positionname, salary, xl, format_time, company, companyid]

        data.append(in_data)
    return data


def get_data_by_city(types, city):
    for type_ in types:
        page = 1
        while True:
            print("正在采集{}{}的第{}页".format(type_, city, page))
            data = get_info_by_type(type_, city, page)
            if len(data) == 0:
                break
            print(data)
            write_to_csv(data)
            page += 1
            # 测试两页
            if page == 2:
                break


def get_all_data():
    citys = get_city()
    types = get_type()
    for city in citys:
        get_data_by_city(types, city)


def read():
    df = pd.read_csv('data_clean.csv')

    count = {}

    for idx in df.index:
        item = df.loc[idx].values[1:]
        if item[-2] not in count:
            count[item[-2]] = [1, [item, ]]
        else:
            count[item[-2]][0] += 1
            count[item[-2]][1].append(item)

    data = list(count.items())
    data.sort(key=lambda x: x[-1][0], reverse=True)
    top15 = data[:15]

    Bar().add_xaxis([item[0] for item in top15]) \
        .add_yaxis('招聘数量', [item[-1][0] for item in top15]) \
        .render('招聘数量.html')
    for item in top15:
        print('*' * 20, item[0], '*' * 20)
        for job in item[1][-1]:
            print(job)
    Funnel().add("商品", top15).set_global_opts().render("funnel_base.html")

def clean():
    df = pd.read_csv('data.csv')
    df.drop_duplicates().fillna(0).to_csv('data_clean.csv', encoding='utf8')


if __name__ == '__main__':
    get_all_data()
    clean()
    read()
