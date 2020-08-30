# https://music.douban.com/tag/
# 5-6个标签
# 歌曲名 歌手 日期 评分 评价人数
import time

import requests, csv
from bs4 import BeautifulSoup
from pyecharts.charts import Pie, Bar, Scatter3D, Scatter, Line
from pyecharts import options as opts

tags = ['OST', '民谣', '流行', 'pop', 'indie', 'Electronic', 'Folk', '摇滚', 'J-POP', 'rock', '电影原声', 'R&B','中国摇滚','纯音乐'][:9]
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
url_demo = 'https://music.douban.com/tag/{}?start={}&type=T'

# 获取html源代码
def get_html(url):
    r = requests.get(url, headers=header)
    html = r.text
    return html

# 找class=pl2下的a的内容
def get_song_name(soup):
    div = soup.find('div', attrs={'class': "pl2"})
    a = div.find('a')
    if a:
        return a.text.replace(' ', '').replace('\n', '')
    return '空标题'

# 找class=pl2下的p的内容/分割第一个
def get_song_author(soup):
    div = soup.find('div', attrs={'class': "pl2"})
    p = div.find('p')
    if p:
        texts = p.text.split('/')
        if len(texts) != 0:
            return texts[0].strip()
    return '空作者'


# 找class=pl2下p的/分割第2个
def get_song_date(soup):
    div = soup.find('div', attrs={'class': "pl2"})
    p = div.find('p')
    if p:
        texts = p.text.split('/')
        if len(texts) >= 2:
            return texts[1].strip()
    return '空时间'

# 找class=rating_nums 的span的内容
def get_song_rank(soup):
    span = soup.find('span', attrs={'class': "rating_nums"})
    if span:
        return span.text
    return '空评分'

# 找class=pl2下的class=pl的span
def get_song_comment_count(soup):
    div = soup.find('div', attrs={'class': "pl2"})
    if div:
        span = div.find('span', attrs={'class': 'pl'})
        if span:
            # 替换无效的字符
            return span.text.replace(' ', '').replace('(', '').replace(')', '').replace('\n', '')
    return '空评论人数'

# 根据偏移量获取数据
def get_songs_by_offset(tag, page):
    songs = []
    # 设置完整url
    url = url_demo.format(tag, page)
    print(url)
    # 获取html源码
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    # 找class=item 的tr数组
    items = soup.find_all('tr', attrs={'class': 'item'})
    # 没找到返回空
    if len(items) == 0:
        return songs
    # 遍历每一个tr
    for item in items:
        # 传tr，让函数获取其中的内容
        name = get_song_name(item)
        author = get_song_author(item)
        date = get_song_date(item)
        rank = get_song_rank(item)
        comment_count = get_song_comment_count(item)
        # 组合成一个数据
        song = (name, author, date, rank, comment_count)
        print(song)
        # 添加每一条，到一页数据的数组
        songs.append(song)
    return songs

# 根据tag采集内容
def get_songs_by_tag(tag):
    offset = 0 #初始偏移量0
    page = 1 #初始页数
    while True:
        print("正在采集", page, '页')
        #获取每页数据
        songs_ = get_songs_by_offset(tag, offset)
        if len(songs_) == 0:
            print('tag采集结束')
            break
        print("第{}页采集成功".format(page))
        # 将数据写入文件
        write_many_to_csv(songs_, tag)
        # 下一页的偏差
        offset += 20
        page += 1

        if page == 2: #采集两页测试
            break
        #程序暂停5秒
        time.sleep(5)


def write_many_to_csv(songs, tag):
    #打开csv文件
    with open(tag + '_songs.csv', 'a', encoding='utf8') as f:
        writer = csv.writer(f)
        #将数组写入csv
        writer.writerows(songs)

#获取全部数据
def get_songs():
    for tag in tags:
        print("采集", tag)
        get_songs_by_tag(tag)

#根据tag获取文件内容
def read(tag):
    data = []
    with open(tag + '_songs.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for item in reader:
            if item:
                data.append(item)
    return data


def draw1():
    counts = {}
    # 遍历每一个tag
    for tag in tags:
        #获取每一个tag的数据
        data = read(tag)
        #获取数据的长度
        count = len(data)
        #记录每个tag有多少数据
        counts[tag] = count
    #生成图
    Pie().add('', list(counts.items())).render('1.html')


def filt(x):
    try:
        #将x转为数字，失败则返回0
        return float(x)
    except:
        return 0


def draw2():
    data_ = []
    for tag in tags:
        #根据tag获取数据
        data = read(tag)
        #提取数据中的名字和评论数，组成新数据
        data_.extend([(x[0], filt(x[-1][:-3])) for x in data])
    #按评论数排序
    data = sorted(data_, key=lambda x: x[-1], reverse=True)[:30]
    #生成图
    bar = Bar()
    bar.add_xaxis([item[0] for item in data])
    bar.add_yaxis("评论数", [item[1] for item in data])
    bar.set_global_opts(title_opts=opts.TitleOpts(title="歌曲评论"))
    bar.render('2.html')

def draw3():
    data_ = []
    for tag in tags:
        # 根据tag获取数据
        data = read(tag)
        # 提取数据中的名字和评论数，组成新数据
        data_.extend([(x[0], filt(x[-1][:-3])) for x in data])
    # 按评论数排序
    data = sorted(data_, key=lambda x: x[-1], reverse=True)[:30]
    # 生成图
    Scatter().add_xaxis(xaxis_data=[item[0] for item in data]).add_yaxis(
        series_name="",
        y_axis=[item[1] for item in data],
        symbol_size=20,
        label_opts=opts.LabelOpts(is_show=False),
    ).render('3.html')

def draw4():
    data_ = []
    for tag in tags:
        # 根据tag获取数据
        data = read(tag)
        # 提取数据中的名字和评论数，组成新数据
        data_.extend([(x[0], filt(x[-1][:-3])) for x in data])
    # 按评论数排序
    data = sorted(data_, key=lambda x: x[-1], reverse=True)[:30]
    # 生成图
    Line().add_xaxis(xaxis_data=[item[0] for item in data]).add_yaxis(
        series_name="",
        y_axis=[item[1] for item in data],
        symbol="emptyCircle",
        is_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=False),
        areastyle_opts=opts.AreaStyleOpts(opacity=1, color="#C67570"),
    ).render('4.html')



def draw5():
    data_ = []
    for tag in tags:
        # 根据tag获取数据
        data =read(tag)
        # 提取数据中的名字和时间，组成新数据
        data_.extend([(x[0] ,x[2]) for x in data])
    #根据时间排序
    data = sorted(data_, key=lambda x: x[-1], reverse=True)
    #日期计数
    dic = ['2000-01-01', '2001-01-01', '2002-01-01', '2003-01-01', '2004-01-01',
           '2005-01-01', '2006-01-01','2007-01-01', '2008-01-01', '2009-01-01',
           '2010-01-01', '2011-01-01','2012-01-01', '2013-01-01', '2014-01-01',
           '2015-01-01', '2016-01-01','2017-01-01', '2018-01-01', '2019-01-01','2020-01-01','2021-01-01']
    count_ = {}
    for item in data:
        for di in dic:
            #获取每一个日期
            if item[-1] < di:
                #日期计数
                if di not in count_:
                    count_[di] = 0
                else:
                    count_[di] += 1
                break
    #生成图
    Pie().add('', list(count_.items())).render('5.html')


if __name__ == '__main__':
    get_songs()
    draw1()
    draw2()
    draw3()
    draw4()
    draw5()
