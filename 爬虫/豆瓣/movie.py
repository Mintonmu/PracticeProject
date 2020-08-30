import time

import requests, json, csv
from pyecharts.charts import Pie, Bar, Scatter, Line

years = ['1960,1969', '1970,1979', '1980,1989', '1990,1999', '2000,2009', '2010,2019', '2020,2020']
url_demo = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start={}&year_range={}'

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


# 获取json数据
def get_json(url):
    # 发起请求
    r = requests.get(url, headers=header)
    try:
        # 解析json数据
        objs = json.loads(r.text)
        # 如果有错误信息，则返回空
        if 'msg' in objs and objs['msg'] == '检测到有异常请求从您的IP发出，请登录再试!':
            print('检测到有异常请求从您的IP发出，请登录再试!')
            return None
        return objs
    except Exception as e:
        print(e)
        return None


# 将数据写入文件
def write_csv(movies, year):
    with open(year + '_movies.csv', 'a', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(movies)


# 根据年份获取数据
def get_movies_by_years(year):
    page = 0
    while True:
        print("采集第{}页".format(page + 1))
        # 组合完整url
        url = url_demo.format(page * 20, year)
        # 获取数据
        data = get_json(url)
        if data:
            # 获取电影数据
            movies_ = data['data']
            # 没获取到则退出
            if len(movies_) == 0:
                break
            movies = []
            # 遍历每一个电影
            for movie_ in movies_:
                # 获取标题
                name = movie_['title']
                # 获取评分
                rank = movie_['rate']
                # 获取导演
                directors = movie_['directors']
                # 获取收藏
                star = movie_['star']
                # 获取演员
                casts = movie_['casts']
                # 组合新数据
                movie = (name, rank, directors, casts, star)
                # 将输入添加到每一页数据组
                movies.append(movie)
                print(movie)
            # 将数据写入文件
            write_csv(movies, year)
        else:
            break
        # 下一页
        page += 1

        if page == 2:  # 采集两页测试
            break
        # 程序暂停5秒
        time.sleep(5)


# 获取每一年数据
def get_movies():
    for year in years:
        print("正在采集", year)
        get_movies_by_years(year)


# 根据文件名获取数据
def read(name):
    data = []
    with open(name, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        # 获取csv每一条数据
        for item in reader:
            if item:
                data.append(item)
    return data


def draw1():
    counts = {}
    for year in years:
        data = read(year + '_movies.csv')
        # 统计每一年电影数量
        count = len(data)
        counts[year] = count
    # 生成图
    Pie().add('', list(counts.items())).render('1.html')


def draw2():
    data_ = []
    for year in years:
        data = read(year + '_movies.csv')
        # 将标题和评分重新组合成新数据
        data_.extend([(x[0], float(x[1])) for x in data])
    # 按评分排序
    data = sorted(data_, key=lambda x: x[-1], reverse=True)[:30]
    # 生成图
    bar = Bar()
    bar.add_xaxis([item[0] for item in data])
    bar.add_yaxis("评分", [item[1] for item in data])
    bar.render('2.html')


def draw3():
    data_ = []
    for year in years:
        data = read(year + '_movies.csv')
        # 将标题和评分重新组合成新数据
        data_.extend([(x[0], float(x[1])) for x in data])
    # 按评分排序
    data = sorted(data_, key=lambda x: x[-1], reverse=True)[:30]
    # 生成图
    Scatter().add_xaxis(xaxis_data=[item[0] for item in data]).add_yaxis(
        series_name="",
        y_axis=[item[1] for item in data],
        symbol_size=20,
    ).render('3.html')


def draw4():
    data_ = []
    for year in years:
        data = read(year + '_movies.csv')
        # 将标题和评分重新组合成新数据
        data_.extend([(x[0], float(x[1])) for x in data])
    # 按评分排序
    data = sorted(data_, key=lambda x: x[-1], reverse=True)[:30]
    # 生成图
    Line().add_xaxis(xaxis_data=[item[0] for item in data]).add_yaxis(
        series_name="",
        y_axis=[item[1] for item in data],
        is_symbol_show=True,
    ).render('4.html')


def draw5():
    data_ = []
    for year in years:
        data = read(year + '_movies.csv')
        # 将标题和评分重新组合成新数据
        data_.extend([(x[0], float(x[-1])) for x in data])
    # 按评分排序
    data = sorted(data_, key=lambda x: x[-1], reverse=True)[:30]
    # 生成图
    bar = Bar()
    bar.add_xaxis([item[0] for item in data])
    bar.add_yaxis("star", [item[1] for item in data])
    bar.render('5.html')


if __name__ == '__main__':
    # 采集
    get_movies()
    # 5个可视化图
    draw1()
    draw2()
    draw3()
    draw4()
    draw5()
