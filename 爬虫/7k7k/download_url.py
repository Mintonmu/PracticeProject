import re

import requests, csv
from bs4 import BeautifulSoup

# 评论
# 下载地址


url_demo = 'http://www.7k7k.com/swf/{:0>6d}.htm'  # 六位数id, 补齐6位

for i in range(100000, 197402):
    url = url_demo.format(i)
    r = requests.get(url, headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'})
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.find('title')  # 找title标签

    if title.text == '404':  # 404页面则跳过
        print('pop', i)
        continue

    link = re.findall(r'_gamepath = "(.*?)"', r.text)
    if len(link) == 0:
        continue

    with open('data.csv', 'a') as f:  # 写入csv
        writer = csv.writer(f)  # 创建写入对象
        row = [link[0], ]  # 预处理
        writer.writerow(row)  # 写入一行
    print(link[0])  # log打印
