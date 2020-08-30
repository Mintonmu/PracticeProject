import pandas as pd
import requests, csv
from bs4 import BeautifulSoup
from pyecharts.charts import *

url_demo = 'https://www.lagou.com/zhaopin/{}/{}/?labelWords=label'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
china = {'河北': ['石家庄', '唐山', '秦皇岛', '邯郸', '邢台', '保定', '张家口', '承德', '沧州', '廊坊', '衡水'],
         '山西': ['太原', '大同', '阳泉', '长治', '晋城', '朔州', '晋中', '运城', '忻州', '临汾', '吕梁'],
         '内蒙古': ['呼和浩特', '包头', '乌海', '赤峰', '通辽', '鄂尔多斯', '呼伦贝尔', '巴彦淖尔', '乌兰察布', '兴安', '锡林郭勒', '阿拉善'],
         '辽宁': ['沈阳', '大连', '鞍山', '抚顺', '本溪', '丹东', '锦州', '营口', '阜新', '辽阳', '盘锦', '铁岭', '朝阳', '葫芦岛'],
         '吉林': ['长春', '吉林', '四平', '辽源', '通化', '白山', '松原', '白城', '延边'],
         '黑龙江': ['哈尔滨', '齐齐哈尔', '鸡西', '鹤岗', '双鸭山', '大庆', '伊春', '佳木斯', '七台河', '牡丹江', '黑河', '绥化', '大兴安岭'],
         '江苏': ['南京', '无锡', '徐州', '常州', '苏州', '南通', '连云港', '淮安', '盐城', '扬州', '镇江', '泰州', '宿迁'],
         '浙江': ['杭州', '宁波', '温州', '嘉兴', '湖州', '绍兴', '金华', '衢州', '舟山', '台州', '丽水'],
         '安徽': ['合肥', '芜湖', '蚌埠', '淮南', '马鞍山', '淮北', '铜陵', '安庆', '黄山', '滁州', '阜阳', '宿州', '六安', '亳州', '池州', '宣城'],
         '福建': ['福州', '厦门', '莆田', '三明', '泉州', '漳州', '南平', '龙岩', '宁德'],
         '江西': ['南昌', '景德镇', '萍乡', '九江', '新余', '鹰潭', '赣州', '吉安', '宜春', '抚州', '上饶'],
         '山东': ['济南', '青岛', '淄博', '枣庄', '东营', '烟台', '潍坊', '济宁', '泰安', '威海', '日照', '莱芜', '临沂', '德州', '聊城', '滨州', '菏泽'],
         '河南': ['郑州', '开封', '洛阳', '平顶山', '安阳', '鹤壁', '新乡', '焦作', '濮阳', '许昌', '漯河', '三门峡', '南阳', '商丘', '信阳', '周口',
                '驻马店'],
         '湖北': ['武汉', '黄石', '十堰', '宜昌', '襄阳', '鄂州', '荆门', '孝感', '荆州', '黄冈', '咸宁', '随州', '恩施'],
         '湖南': ['长沙', '株洲', '湘潭', '衡阳', '邵阳', '岳阳', '常德', '张家界', '益阳', '郴州', '永州', '怀化', '娄底', '湘西'],
         '广东': ['广州', '韶关', '深圳', '珠海', '汕头', '佛山', '江门', '湛江', '茂名', '肇庆', '惠州', '梅州', '汕尾', '河源', '阳江', '清远', '东莞',
                '中山', '潮州', '揭阳', '云浮'],
         '广西': ['南宁', '柳州', '桂林', '梧州', '北海', '防城港,钦州,贵港', '玉林', '百色', '贺州', '河池', '来宾', '崇左'],
         '海南': ['海口', '三亚', '三沙', '儋州'],
         '四川': ['成都', '自贡', '攀枝花', '泸州', '德阳', '绵阳', '广元', '遂宁', '内江', '乐山', '南充', '眉山', '宜宾', '广安', '达州', '雅安', '巴中',
                '资阳', '阿坝', '甘孜', '凉山'],
         '贵州': ['贵阳', '六盘水', '遵义', '安顺', '毕节', '铜仁', '黔西南', '黔东南', '黔南'],
         '云南': ['昆明', '曲靖', '玉溪', '保山', '昭通', '丽江', '普洱', '临沧', '楚雄', '红河', '文山', '西双版纳', '大理', '德宏', '怒江', '迪庆'],
         '西藏': ['拉萨', '日喀则', '昌都', '林芝', '山南', '那曲', '阿里'],
         '陕西': ['西安', '铜川', '宝鸡', '咸阳', '渭南', '延安', '汉中', '榆林', '安康', '商洛'],
         '甘肃': ['兰州', '嘉峪关', '金昌', '白银', '天水', '武威', '张掖', '平凉', '酒泉', '庆阳', '定西', '陇南', '临夏', '甘南'],
         '青海': ['西宁', '海东', '海北', '黄南', '海南', '果洛', '玉树', '海西'],
         '宁夏': ['银川', '石嘴山', '吴忠', '固原', '中卫'],
         '新疆': ['乌鲁木齐', '克拉玛依', '吐鲁番', '哈密', '昌吉', '博尔塔拉', '巴音郭楞', '阿克苏', '克孜勒苏柯尔克孜', '喀什', '和田', '伊犁哈萨克', '塔城', '阿勒泰'],
         '北京': ['北京'],
         '上海': ['上海'],
         '重庆': ['重庆'],
         '天津': ['天津']
         }


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

#根据分类和城市采集
def get_data_by_city(types, city):
    # 遍历分类
    for type_ in types:
        # 页数
        page = 1
        while True:
            print("正在采集{}{}的第{}页".format(type_, city, page))
            data = get_info_by_type(type_, city, page)
            # 如果采集到空则结束
            if len(data) == 0:
                break
            print(data)
            write_to_csv(data)
            page += 1
            # 测试两页
            if page == 2:
                break

# 爬虫执行函数
def get_all_data():
    citys = get_city()
    types = get_type()
    # 遍历每一个城市的职业
    for city in citys:
        get_data_by_city(types, city)


def read():
    df = pd.read_csv('data_clean.csv')
    map_data = {}

    for idx in df.index:
        item = df.loc[idx].values[1:]
        prov = '北京'
        for key in china:
            # 获取城市对应的省份
            if item[0] in china[key]:
                prov = key

        # 统计每一个省份的职业
        if prov not in map_data:
            map_data[prov] = []
        else:
            map_data[prov].append(item)

    for key in map_data:
        map_data[key] = len(map_data[key])
    Map().add("", list(map_data.items()), "china").render(
        "map_base.html")


def clean():
    df = pd.read_csv('data.csv')
    df.drop_duplicates().fillna(0).to_csv('data_clean.csv', encoding='utf8')


if __name__ == '__main__':
    get_all_data()
    clean()
    read()
