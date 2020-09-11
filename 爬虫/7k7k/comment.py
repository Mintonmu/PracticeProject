import json

import requests, csv, re
from bs4 import BeautifulSoup
import pyecharts.options as opts
from pyecharts.charts import WordCloud

url_demo = 'http://www.7k7k.com/flash/{:0>6d}.htm'
header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}

comment_demo = 'http://changyan.sohu.com/node/html?client_id=cyqHvdkcp&topicsid=7k7kmainsite{:0>6d}'  # 六位数id, 补齐6位

# 预处理
def filter_emoji(desstr, restr=''):
    # 过滤表情
    co = re.compile('[^\u4e00-\u9fa5]')
    return co.sub(restr, desstr)


def write(data):
    with open('data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([data, ])


# 爬虫
def pa():
    for i in range(100000, 197402):
        url = url_demo.format(i)
        r = requests.get(url, headers=header)

        soup = BeautifulSoup(r.text, 'lxml')
        title = soup.find('title')  # 找title标签

        if title.text == '404':  # 404页面则跳过
            print('pop', i)
            continue

        url = comment_demo.format(i)
        r = requests.get(url, headers=header)
        jt = json.loads(r.text)
        comments = jt['listData']['comments']
        comment_content = []
        for comment in comments:
            comment_content.append(comment['content'])
        if len(comment_content) != 0:
            print(comment_content)
            write(str(comment_content))


# 可视化
def word():
    w = WordCloud()

    import jieba
    txt = ''
    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            txt += filter_emoji(row[0]).replace('[', '').replace(']', '').replace(' ', '').replace(' ', '').replace("'",
                                                                                                                    '').replace(
                ',', '')
    txt = jieba.lcut(txt)

    count = {}
    for wo in txt:
        if wo in count:
            count[wo] += 1
        else:
            count[wo] = 1

    w.add(series_name="热点分析", data_pair=list(count.items()), word_size_range=[6, 66])

    w.set_global_opts(
        title_opts=opts.TitleOpts(
            title="热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True),
    )
    w.render()




if __name__ == '__main__':
    word()
