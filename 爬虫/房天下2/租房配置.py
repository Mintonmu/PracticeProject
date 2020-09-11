# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re, time, csv
import pyecharts.options as opts

from pyecharts.charts import Pie, Scatter3D, Line, Grid, Map
from pyecharts.commons.utils import JsCode

city = ['北京', '上海', '广东', '深圳', '沈阳', '大连']
e_city = ['beijing', 'shanghai', 'guangdong', 'shenzheng', 'shenyang', 'dalian']
eshouse = ['https://zu.fang.com/house/i3{}/', 'https://sh.zu.fang.com/house/i3{}/',
           'https://gz.zu.fang.com/house/i3{}/', 'https://sz.zu.fang.com/house/i3{}/',
           'https://sy.zu.fang.com/house/i3{}/', 'https://dl.zu.fang.com/house/i3{}/']

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}


def write_to_csv(houses, city):
    with open(city + '.csv', 'a', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(houses)


def read_from_csv(city):
    with open(city + '.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def run(url_demo, city_id, page):
    print("{}, 第{}页".format(city[city_id], page))
    url = url_demo.format(page)

    soup = get_real(url)

    names = []
    for name in soup.find_all('dd', attrs={'class': 'info rel'}):
        names.append(name.p.a.text.strip())
    if not names:
        return False

    eq = []
    for item in soup.find_all('p', attrs={'class': 'font15 mt12 bold'}):
        li = item.text.strip().split('|')
        eq.append(li[1])

    moneys = []
    for item in soup.find_all('p', attrs={'class': 'mt5 alingC'}):
        moneys.append(item.text)

    houses = []
    for idx in range(len(names)):
        try:
            item = [names[idx], moneys[idx], eq[idx]]
            houses.append(item)
        except Exception as e:
            print(e)

    write_to_csv(houses, e_city[city_id])

    return True


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
    for idx in range(len(e_city)):

        url = eshouse[idx]
        soup = get_real(url.format(2))
        try:
            page_number = int(soup.find('div', attrs={'id': 'rentid_D10_01'}).find_all('span')[-1].text[1:-1])
            pages = page_number
        except:
            pages = 100

        for page in range(1, pages + 1):
            ans = run(url, idx, page)
            if not ans:
                break


def draw():
    data = list(map(lambda x: x[-2], read_from_csv('beijing')))

    count = {'0-2000': 0, '2000-4000': 0, '4000-6000': 0, '6000-8000': 0, '8000-10000': 0, '10000+': 0}

    for item in data:
        price = float(item[:-3])

        if price <= 2000:
            count['0-2000'] += 1
        elif price <= 4000:
            count['2000-4000'] += 1
        elif price <= 6000:
            count['4000-6000'] += 1
        elif price <= 8000:
            count['8000-10000'] += 1
        else:
            count['10000+'] += 1

    Pie().add('', list(count.items())).render()


def draw1():
    houses = []
    for filename in [c + '.csv' for c in e_city]:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[-1] != '价格待定':
                    houses.append(row)

    houses = list(map(lambda x: (x[0], x[-2].split('元/月')[0]), houses))

    count = {'0-2000': 0, '2000-4000': 0, '4000-6000': 0, '6000-8000': 0, '8000-10000': 0, '10000+': 0}

    for item in houses:
        price = float(item[-1])

        if price <= 2000:
            count['0-2000'] += 1
        elif price <= 4000:
            count['2000-4000'] += 1
        elif price <= 6000:
            count['4000-6000'] += 1
        elif price <= 8000:
            count['8000-10000'] += 1
        else:
            count['10000+'] += 1


    background_color_js = (
        "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
        "[{offset: 0, color: '#c86589'}, {offset: 1, color: '#06a7ff'}], false)"
    )
    area_color_js = (
        "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
        "[{offset: 0, color: '#eb64fb'}, {offset: 1, color: '#3fbbff0d'}], false)"
    )

    c = (
        Line(init_opts=opts.InitOpts(bg_color=JsCode(background_color_js)))
            .add_xaxis(xaxis_data=list(count.keys()))
            .add_yaxis(
            series_name="",
            y_axis=list(count.values()),
            is_smooth=True,
            is_symbol_show=True,
            symbol="circle",
            symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(color="#fff"),
            label_opts=opts.LabelOpts(is_show=True, position="top", color="white"),
            itemstyle_opts=opts.ItemStyleOpts(
                color="red", border_color="#fff", border_width=3
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            areastyle_opts=opts.AreaStyleOpts(color=JsCode(area_color_js), opacity=1),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="",
                pos_bottom="5%",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=16),
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                boundary_gap=False,
                axislabel_opts=opts.LabelOpts(margin=30, color="#ffffff63"),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=25,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                position="right",
                axislabel_opts=opts.LabelOpts(margin=20, color="#ffffff63"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=2, color="#fff")
                ),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=15,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    (
        Grid()
            .add(
            c,
            grid_opts=opts.GridOpts(
                pos_top="20%",
                pos_left="10%",
                pos_right="10%",
                pos_bottom="15%",
                is_contain_label=True,
            ),
        )
            .render("beautiful_line_chart.html")
    )




def draw2():

    count = {}
    for c in e_city:
        with open(c + '.csv', 'r') as f:
            c = city[e_city.index(c)]
            count[c] = 0
            reader = csv.reader(f)
            for row in reader:
                if row[-1] != '价格待定':
                    count[c] += 1
    (
        Map()
        .add(
            series_name="城市租房分布",
            data_pair=list(count.items()),
            is_map_symbol_show=False,
        )
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(
                min_=100,
                max_=300,
                range_text=["High", "Low"],
                is_calculable=True,
                range_color=["lightskyblue", "yellow", "orangered"],
            ),
        )
        .render("全国租房分布.html")
    )


if __name__ == '__main__':
    # 采集
    # craw()
    # 词云
    draw1()
    draw2()