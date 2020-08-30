import re

import jieba
import requests, csv, time
from bs4 import BeautifulSoup
from pyecharts.charts import Pie, Bar


# 将数组写入文件
def write(items):
    with open('tiezi.csv', 'a', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(items)


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
types = ['', '/culture', '/travel', '/ent', '/fashion', '/life', '/tech']
types_name = ['精选', '文化', '行摄', '娱乐', '时尚', '生活', '科技']


def catch():
    # 遍历每一个类型
    for type_, name in zip(types, types_name):
        print("采集", name)
        page = 0
        # 无限循环
        while True:
            print("采集第{}页".format(page + 1))
            # 生成完整url
            url = 'https://www.douban.com/group/explore{}?start={}'.format(type_, page * 30)
            r = requests.get(url, headers=header)
            soup = BeautifulSoup(r.text, 'lxml')
            # 查找class=channel-item的div
            items = soup.find_all('div', attrs={'class': 'channel-item'})
            # 采集到空数据，则返回
            if len(items) == 0:
                print(str(soup))
                break
            docs = []
            # 遍历div
            for item in items:
                # 找class=bd的div下的a
                a = item.find('div', attrs={'class': 'bd'}).a
                # 获取a的内容
                title = a.text
                # 获取a的href
                src = a.attrs['href']
                # 获取div下的div的内容，去掉最后两个字符
                like = item.find('div').text[:-2]
                # 获取class=from的span的内容，去掉开头两个字符
                source = item.find('span', attrs={'class': "from"}).text[2:]
                # 获取class=pubtime的span的内容
                time_ = item.find('span', attrs={'class': 'pubtime'}).text
                # 组成新数据
                it = (title, src, like, source, time_, name)
                print(it)
                # 添加每一条数据到每一页数据中
                docs.append(it)
            # 将每一页数据写入
            write(docs)
            # 下一页
            page += 1

            if page == 2:  # 采集两页测试
                break
            # 程序暂停3秒
            time.sleep(3)


# 从文件获取数据
def read():
    data = []
    with open('tiezi.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for item in reader:
            if item:
                data.append(item)
    return data


def draw1():
    count = {'精选': 0, '文化': 0, '行摄': 0, '娱乐': 0, '时尚': 0, '生活': 0, '科技': 0}

    data = read()
    for item in data:
        # 对数据的最后一项进行计数
        if item[-1]:
            count[item[-1]] += 1
        else:
            count['精选'] += 1

    Pie().add("帖子分类", list(count.items())).render("帖子分类.html")


def draw2():
    count = {}
    data = read()

    for item in data:
        # 对数据的最后第三项进行计数
        if item[-3] not in count:
            count[item[-3]] = 1
        else:
            count[item[-3]] += 1

    from pyecharts import options as opts
    # 获取字典每一项
    data = list(count.items())
    # 按计数数量排序
    sorted(data, key=lambda x: x[-1])
    # 生成图片
    Pie(init_opts=opts.InitOpts()).add("小组分类", data[:10]).render("小组分类.html")


def draw3():
    data = read()
    # 按link数量排序
    data.sort(key=lambda x: x[2], reverse=True)
    # 生成图片
    Bar().add_xaxis([item[0] for item in data[:10]]).add_yaxis("link", [float(item[2]) for item in data[:10]]).render(
        "喜欢人数.html")


def draw4():
    count = {'0-100': 0, '100-200': 0, '200-300': 0, '300-400': 0, '400-500': 0, '500-600': 0, '600-700': 0,
             '700-800': 0, '800-900': 0, '900-1000': 0}
    data = read()

    for item in data:
        # 获取 喜欢数量，按数量分布计数
        like = float(item[2])
        if like <= 100:
            count['0-100'] += 1
        elif like <= 200:
            count['100-200'] += 1
        elif like <= 300:
            count['200-300'] += 1
        elif like <= 400:
            count['300-400'] += 1
        elif like <= 500:
            count['400-500'] += 1
        elif like <= 600:
            count['500-600'] += 1
        elif like <= 700:
            count['600-700'] += 1
        elif like <= 800:
            count['700-800'] += 1
        elif like <= 900:
            count['800-900'] += 1
        elif like <= 1000:
            count['900-1000'] += 1

    Pie().add("", list(count.items())).render("收藏分布.html")


def draw5():
    seq = ''
    data = read()
    # 将标题全部组合
    for item in data:
        seq += item[0]
    # 提取其中中文
    str = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", seq)
    m = re.findall('[\u4e00-\u9fa5]', str)
    # 分词
    lit = list(jieba.cut(''.join(m)))
    # 统计中文字频
    count = {}
    for it in lit:
        if it not in count:
            count[it] = 1
        else:
            count[it] += 1
    # 生成图
    from pyecharts.charts import WordCloud
    WordCloud().add('', list(count.items())).render("词云.html")


if __name__ == '__main__':
    catch()
    draw1()
    draw2()
    draw3()
    draw4()
    draw5()
