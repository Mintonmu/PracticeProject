import requests, csv
from bs4 import BeautifulSoup


# 评论
# 下载地址
# 名字 大小 类别

# 爬虫
def grab():
    url_demo = 'http://www.7k7k.com/flash/{:0>6d}.htm'  # 六位数id, 补齐6位

    for i in range(100000, 197402):
        url = url_demo.format(i)
        r = requests.get(url, headers={
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'})
        soup = BeautifulSoup(r.text, 'lxml')
        title = soup.find('title')  # 找title标签

        if title.text == '404':  # 404页面则跳过
            print('pop', i)
            continue

        div = soup.find('div', attrs={'class': 'game-meta'})  # 找class=game-meta, div标签
        if div:
            spans = div.find_all('span', attrs={'class': "item"})  # 从div中找class=item 的span
            div = soup.find('div', attrs={'id': 'game-info'})  # 找id=game-info， div的标签
            title = div.h1.a.text  # 获取div下h1标签下a标签的内容
            type_ = spans[1].text[3:]  # 获取第1个span标签的从3开始的字符
            size = spans[2].text[3:]  # 获取第2个span标签的从3开始的字符
            item = (title, type_, size)  # 组成一行
            with open('data.csv', 'a') as f:  # 写入csv
                writer = csv.writer(f)  # 创建写入对象
                writer.writerow(item)  # 写入一行
            print(item)  # log打印


# 可视化
def show():
    from pyecharts import options as opts
    from pyecharts.charts import Pie, Bar, Funnel, Line
    count = {}
    size_ = {'0M-1M':0,'1M-10M':0,'10M-50M':0, '50M-100M':0,'100M-':0}
    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        for item in reader:
            # 预处理
            size = float(item[-1][:-1])
            if size<=1:
                size_['0M-1M'] += 1
            elif size <=10:
                size_['1M-10M'] += 1
            elif size <=50:
                size_['10M-50M'] +=1
            elif size <= 100:
                size_['50M-100M'] +=1
            else:
                size_['100M-'] +=1

            if item[1] in count:
                count[item[1]] += 1
            else:
                count[item[1]] = 0

    Pie().add("", list(count.items())).set_global_opts(title_opts=opts.TitleOpts(title="Pie")).set_series_opts(
        label_opts=opts.LabelOpts(formatter="{b}: {c}")).render("pie.html")

    Bar().add_xaxis(list(count.keys())).add_yaxis("数量", count.values()).set_global_opts(title_opts=opts.TitleOpts(title="Bar")).render("bar.html")

    Line().add_xaxis(xaxis_data=list(size_.keys())).add_yaxis(
        series_name="",
        y_axis=size_.values()
    ).render("line.html")

    Funnel().add("", list(count.items())).set_global_opts(title_opts=opts.TitleOpts(title="Funnel")).render("funnel.html")

if __name__ == '__main__':
    show()
    #grab()
