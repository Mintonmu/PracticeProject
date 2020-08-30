# -*- coding: utf-8 -*-
from sys import path

import requests
from bs4 import BeautifulSoup
import time
import urllib
import re
import csv
from tqdm import tqdm
from pyecharts.charts.wordcloud import WordCloud
class SNProcess():
    def __init__(self):
        self.last_good = ''
        brands_dic, opt_dic, other_opt_dic = self.get_type_code("http://list.suning.com/0-20006-0.html")
        #brand_id, opt_id, o_opt_id = self._input(brands_dic, opt_dic, other_opt_dic)
        brands_values = brands_dic.values()
        
        opt_value = []
        for key, value in opt_dic.items():
            for key1, value1 in value.items():
                opt_value.append(value1)
        o_opt_value = []
        for key, value in other_opt_dic.items():
            for key1, value1 in value.items():
                o_opt_value.append(value1)

        for i in brands_values:
            for j in opt_value:
                for k in o_opt_value:
                    self.run('http://list.suning.com/0-20006-0-{}-0-0-0-0-0-0-{}-{}-{}.html', i, j, k)


        # self.run( 'http://list.suning.com/0-20006-0-{}-0-0-0-0-0-0-{}-{}-{}.html', brand_id, opt_id, o_opt_id)

    def shop(self, src):
        # url = '//product.suning.com/0070574795/11912366396.html?safp=d488778a.13701.productWrap.11&safc=prd.0.0&safpn=10007'
        price = self.get_price_html(src)
        clusterId, title = self.get_goods_title(src)
        ret_data = [title, price]
        print(ret_data)


    def _input(self, brands_dic, opt_dic, other_opt_dic):
        for item in brands_dic.items():
            print(item)
        brand_id = input('输入要抓取的品牌id: ')

        for item in opt_dic.items():
            print(item)
        opt_id = input('输入要抓取的分类id: ')

        for item in other_opt_dic.items():
            print(item)
        o_opt_id = input('输入要抓取的其他分类id: ')

        return brand_id, opt_id, o_opt_id


    def get_html(self, url):
        res = requests.get(url)
        return res.text

    def write_data(self, data):
        with open("sndata.csv", "a+", encoding="utf-8", errors='ignore', newline="") as f:
            f_csv = csv.writer(f)
            f_csv.writerow(data)
    
    def get_goods_title(self, url):
        html = self.get_html("https:" + url)
        soup = BeautifulSoup(html, 'lxml')
        # print(html)
        title = soup.find_all('title')[0].get_text()
        clusterId = re.compile(r'"clusterId":"(.*?)"', re.S)
        clusterId_ret = clusterId.findall(html)
        
        return clusterId_ret[0],title

    def get_price_html(self, goods_src):
        try:
            src_args = re.findall(r"com/(.*?).html", goods_src)[0]
            key0 = src_args.split("/")[0]
            key1 = src_args.split("/")[-1]
            price_src = "https://pas.suning.com/nspcsale_0_0000000" + key1 + "_0000000" + key1 + "_" + key0 + "_250_029_0290199_20089_1000257_9254_12006_Z001___R1901001_0.5_0___000060864___.html?callback=pcData&_=1581050220963"
            html = self.get_html(price_src)
            price = re.compile(r'"netPrice":"(.*?)"', re.S)
            price_ret = price.findall(html)
            return price_ret[0]
        except:
            return -1
    
    def get_comment_num(self, clsid, goods_src):
        src_args = re.findall(r"com/(.*?).html", goods_src)[0]
        key1 = src_args.split("/")[-1]
        if clsid:
            url = "https://review.suning.com/ajax/review_count/cluster-"+str(clsid)+\
              "-0000000"+str(key1)+"-0000000000-----satisfy.htm?callback=satisfy"
        else:
            url = "http://review.suning.com/ajax/review_count/general--0000000"+str(key1)+"-0000000000-----satisfy.htm?callback=satisfy"
        html = self.get_html(url)
        
        totalCount = re.findall(r'"totalCount":(.*?),', html)[0]
        
        return totalCount

    def get_comment_data(self, goods_src, clsid, num, redata):
        redata.append(num)
        src_args = re.findall(r"com/(.*?).html", goods_src)[0]
        key1 = src_args.split("/")[-1]
        page = int(num/10) + 1
        contents = []
        for i in range(page):
            url = "http://review.suning.com/ajax/cluster_review_lists/cluster-"+str(clsid)+"-0000000"+str(key1)+"-0000000000-total-"+str(i+1)+"-default-10-----reviewList.htm?callback=reviewList"
            
            html = self.get_html(url)
            content = re.findall(r'"content":"(.*?)","publishTime', html)
            if len(content) == 0:
                break
            contents.append(content)

        redata.append(contents)
        print(redata)
        self.write_data(redata)

    def get_data(self, html):
        soup = BeautifulSoup(html, 'lxml')
        uls = soup.find_all('ul', attrs={'class': 'general clearfix'})
        if len(uls) == 0:
            print(str(soup))
            return
            
        lis = soup.find_all('ul', attrs={'class': 'general clearfix'})[0].find_all("li")
        for li in lis:
            try:
                src = li.find_all("a", attrs={"target": "_blank"})[0].get("href")
                price = self.get_price_html(src)
                clusterId, title = self.get_goods_title(src)
                ret_data = [title, price]
                totalCount = self.get_comment_num(clusterId, src)
                self.get_comment_data(src, clusterId, int(totalCount), ret_data)
            except:
                print("数据异常")
                continue

    def run(self, url, brand_id, opt_id, o_opt_id):
        print(url.format(0, brand_id, opt_id, o_opt_id))
        try:
            soup = BeautifulSoup(self.get_html(url.format(0, brand_id, opt_id, o_opt_id)), 'lxml').find('div', attrs={'class':'search-page'})
            a = soup.find_all('a')
            if a[-4].text == '说说您使用搜索的感受GO':
                num = int(a[-2].text)
            else:
                num = int(a[-4].text)
        except AttributeError:
            print("没有找到符合条件的商品")
            return
        except IndexError as e:
            num = 1

        for i in range(num):
            html = self.get_html(url.format(i, brand_id, opt_id, o_opt_id))
            self.get_data(html)

    def get_type_code(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        brands = soup.find('ul', attrs={'class': "brands"}).find_all('li', attrs={'class':'s-brand'})
        brands_dic = {}
        opt_dic = {}
        other_opt_dic = {}
        for brand in brands:
            brands_dic[brand.attrs['title']] = brand.attrs['id']
        other_opts = soup.find_all('div', attrs={'class': 'other-opts'})
        opts = soup.find_all('div', attrs={'class':'filter-section'})

        for opt in opts[1:-1]:
            opt_name = opt.find('label').text
            opt_in = opt.find_all('a', attrs={'class': "f-item"})
            dic = {}
            for i in opt_in:
                id = i.attrs['id']
                title = i.attrs['title']
                dic[title] = id
            opt_dic[opt_name] = dic


        for opt in other_opts:
            opt_name = opt.a.text
            opt_in = opt.find_all('a', attrs={'rel': "nofollow"})
            dic = {}
            for i in opt_in:
                id = i.attrs['id']
                title = i.attrs['title']
                dic[title] = id
            other_opt_dic[opt_name] = dic
        return brands_dic, opt_dic, other_opt_dic
 

def render():
    import matplotlib.pyplot as plt
    import jieba
    from wordcloud import WordCloud, STOPWORDS
    content = ''
    with open('sndata.csv', 'r') as f:
        reader = csv.reader(f)
        for item in reader:
            content += item[-1].replace('[','').replace(']','').replace("'",'').replace(',','').replace(' ','').replace('此用户没有填写评价内容','').replace('#','')

    text = " ".join(jieba.cut(content))
    wc = WordCloud(font_path='wqy-microhei.ttc')
    plt.imshow(wc.generate(text))
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    SNProcess()
    render()