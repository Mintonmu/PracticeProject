# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time, json
import urllib
import re
import csv
from tqdm import tqdm

rank_parameter_url = 'http://tuijian.suning.com/recommend-portal/recommend/paramsBiz.jsonp?sceneIds=10-94&count=50' # 获取rank分类参数

rank_good_url = 'https://tuijian.suning.com/recommend-portal/dyBase.jsonp?parameter={}&sceneIds=22-38&count=10' # 获取分类的商品

main_good = 'https://tuijian.suning.com/recommend-portal/dyBase.jsonp?parameter={}&sceneIds=22-29&count=10'
guess_link = 'http://tuijian.suning.com/recommend-portal/dyBase.jsonp?sceneIds=22-34&count=50'
dic = {'苏宁生鲜': 202417, '米面制品': 202424, '苏宁好酒': 202423, '乳品冲饮' : 202422, '纸巾清洁' : 202419, '休闲饮食' : 202426, '苏宁健康' : 202427, '个人护理' : 202418, '美妆' : 202425}


class SNProcess():
    def __init__(self):
        goods = self.get_shop_url()
        self.write_data(goods)

    def write_data(self, data):
        with open("sndata.csv", "a+", encoding="utf-8", errors='ignore', newline="") as f:
            f_csv = csv.writer(f)
            f_csv.writerows(data)

    def get_shop_url(self):
        r = requests.get(rank_parameter_url)
        type_id = json.loads(r.text)['sugGoods'][0]['skus']
        goods = []
        for id in type_id:
            url = rank_good_url.format(id)
            r = requests.get(url)
            goods.extend(json.loads(r.text)['sugGoods'][0]['skus'])
        
        for key in dic:
            r = requests.get(main_good.format(dic[key]))
            goods.extend(json.loads(r.text)['sugGoods'][0]['skus'])
        

        r = requests.get(guess_link)
        goods.extend(json.loads(r.text)['sugGoods'][0]['skus'])
        goods = [[item['sugGoodsName'], item['price']] for item in goods]

        return goods


def pie():
    from pyecharts.charts.pie import Pie
    x = ['0-50', '50-100', '100+']
    y = [0, 0, 0]

    with open('sndata.csv', 'r') as f:
        reader = csv.reader(f)
        for item in reader:
            price = float(item[-1])
            if price <=50:
                y[0] += 1
            elif price <=100:
                y[1] +=1
            else:
                y[2] +=1
    p = Pie()
    p.add("", x, y)
    p.render()


if __name__ == "__main__":
    SNProcess()
    pie()