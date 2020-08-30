import requests, json, time, csv
from bs4 import BeautifulSoup
import threading
from pymongo import MongoClient as Client
import threading
from pyecharts import Pie
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/64.0.3282.186 Safari/537.36',
                        'referer': 'https://www.bilibili.com'}


tid_dic = {'24': ('MAD·AMV', 'mad', ('动画（主分区）', 'douga', '1')), '25': ('MMD·3D', 'mmd', ('动画（主分区）', 'douga', '1')), '47': ('短片·手书·配音', 'voice', ('动画（主分区）', 'douga', '1')), '86': ('特摄', 'tokusatsu', ('动画（主分区）', 'douga', '1')), '27': ('综合', 'other', ('动画（主分区）', 'douga', '1')), '1': ('动画（主分区）', 'douga', None), '33': ('连载动画', 'serial', ('番剧（主分区）', 'anime', '13')), '32': ('完结动画', 'finish', ('番剧（主分区）', 'anime', '13')), '51': ('资讯', 'information', ('番剧（主分区）', 'anime', '13')), '152': ('官方延伸', 'offical', ('番剧（主分区）', 'anime', '13')), '13': ('番剧（主分区）', 'anime', None), '153': ('国产动画', 'chinese', ('国创（主分区）', 'guochuang', '167')), '168': ('国产原创相关', 'original', ('国创（主分区）', 'guochuang', '167')), '169': ('布袋戏', 'puppetry', ('国创（主分区）', 'guochuang', '167')), '195': ('动态漫·广播剧', 'motioncomic', ('国创（主分区）', 'guochuang', '167')), '170': ('资讯', 'information', ('国创（主分区）', 'guochuang', '167')), '167': ('国创（主分区）', 'guochuang', None), '28': ('原创音乐', 'original', ('音乐（主分区）', 'music', '3')), '31': ('翻唱', 'cover', ('音乐（主分区）', 'music', '3')), '30': ('VOCALOID·UTAU', 'vocaloid', ('音乐（主分区）', 'music', '3')), '194': ('电音', 'electronic', ('音乐（主分区）', 'music', '3')), '59': ('演奏', 'perform', ('音乐（主分区）', 'music', '3')), '193': ('MV', 'mv', ('音乐（主分区）', 'music', '3')), '29': ('音乐现场', 'live', ('音乐（主分区）', 'music', '3')), '130': ('音乐综合', 'other', ('音乐（主分区）', 'music', '3')), '3': ('音乐（主分区）', 'music', None), '20': ('宅舞', 'otaku', ('舞蹈（主分区）', 'dance', '129')), '198': ('街舞', 'hiphop', ('舞蹈（主分区）', 'dance', '129')), '199': ('明星舞蹈', 'star', ('舞蹈（主分区）', 'dance', '129')), '200': ('中国舞', 'china', ('舞蹈（主分区）', 'dance', '129')), '154': ('舞蹈综合', 'three_d', ('舞蹈（主分区）', 'dance', '129')), '156': ('舞蹈教程', 'demo', ('舞蹈（主分区）', 'dance', '129')), '129': ('舞蹈（主分区）', 'dance', None), '17': ('单机游戏', 'stand_alone', ('游戏（主分区）', 'game', '4')), '171': ('电子竞技', 'esports', ('游戏（主分区）', 'game', '4')), '172': ('手机游戏', 'mobile', ('游戏（主分区）', 'game', '4')), '65': ('网络游戏', 'online', ('游戏（主分区）', 'game', '4')), '173': ('桌游棋牌', 'board', ('游戏（主分区）', 'game', '4')), '121': ('GMV', 'gmv', ('游戏（主分区）', 'game', '4')), '136': ('音游', 'music', ('游戏（主分区）', 'game', '4')), '19': ('Mugen', 'mugen', ('游戏（主分区）', 'game', '4')), '4': ('游戏（主分区）', 'game', None), '201': ('科学科普', 'science', ('知识（主分区）', 'technology', '36')), '124': ('社科人文（趣味科普人文）', 'fun', ('知识（主分区）', 'technology', '36')), '207': ('财经', 'finance', ('知识（主分区）', 'technology', '36')), '208': ('校园学习', 'campus', ('知识（主分区）', 'technology', '36')), '209': ('职业职场', 'career', ('知识（主分区）', 'technology', '36')), '122': ('野生技术协会', 'wild', ('知识（主分区）', 'technology', '36')), '39': ('演讲·公开课（目前已下线）', 'speech_course', ('知识（主分区）', 'technology', '36')), '96': ('星海（目前已下线）', 'military', ('知识（主分区）', 'technology', '36')), '98': ('机械（目前已下线）', 'mechanical', ('知识（主分区）', 'technology', '36')), '36': ('知识（主分区）', 'technology', None), '95': ('手机平板', 'mobile', ('数码（主分区）', 'digital', '188')), '189': ('电脑装机', 'pc', ('数码（主分区）', 'digital', '188')), '190': ('摄影摄像', 'photography', ('数码（主分区）', 'digital', '188')), '191': ('影音智能', 'intelligence_av', ('数码（主分区）', 'digital', '188')), '188': ('数码（主分区）', 'digital', None), '138': ('搞笑', 'funny', ('生活（主分区）', 'life', '160')), '21': ('日常', 'daily', ('生活（主分区）', 'life', '160')), '76': ('美食圈', 'food', ('生活（主分区）', 'life', '160')), '75': ('动物圈', 'animal', ('生活（主分区）', 'life', '160')), '161': ('手工', 'handmake', ('生活（主分区）', 'life', '160')), '162': ('绘画', 'painting', ('生活（主分区）', 'life', '160')), '163': ('运动', 'sports', ('生活（主分区）', 'life', '160')), '176': ('汽车', 'automobile', ('生活（主分区）', 'life', '160')), '174': ('其他', 'other', ('生活（主分区）', 'life', '160')), '160': ('生活（主分区）', 'life', None), '22': ('鬼畜调教', 'guide', ('鬼畜（主分区）', 'kichiku', '119')), '26': ('音MAD', 'mad', ('鬼畜（主分区）', 'kichiku', '119')), '126': ('人力VOCALOID', 'manual_vocaloid', ('鬼畜（主分区）', 'kichiku', '119')), '127': ('教程演示', 'course', ('鬼畜（主分区）', 'kichiku', '119')), '119': ('鬼畜（主分区）', 'kichiku', None), '157': ('美妆', 'makeup', ('时尚（主分区）', 'fashion', '155')), '158': ('服饰', 'clothing', ('时尚（主分区）', 'fashion', '155')), '164': ('健身', 'aerobics', ('时尚（主分区）', 'fashion', '155')), '159': ('T台', 'catwalk', ('时尚（主分区）', 'fashion', '155')), '192': ('风尚标', 'trends', ('时尚（主分区）', 'fashion', '155')), '155': ('时尚（主分区）', 'fashion', None), '203': ('热点', 'hotspot', ('资讯（主分区）', 'information', '202')), '204': ('环球', 'global', ('资讯（主分区）', 'information', '202')), '205': ('社会', 'social', ('资讯（主分区）', 'information', '202')), '206': ('综合', 'multiple', ('资讯（主分区）', 'information', '202')), '202': ('资讯（主分区）', 'information', None), '166': ('广告', 'ad', ('广告（主分区）', 'ad', '165')), '165': ('广告（主分区）', 'ad', None), '71': ('综艺', 'variety', ('娱乐（主分区）', 'ent', '5')), '137': ('明星', 'star', ('娱乐（主分区）', 'ent', '5')), '131': ('Korea相关', 'korea', ('娱乐（主分区）', 'ent', '5')), '5': ('娱乐（主分区）', 'ent', None), '182': ('影视杂谈', 'cinecism', ('影视（主分区）', 'cinephile', '181')), '183': ('影视剪辑', 'montage', ('影视（主分区）', 'cinephile', '181')), '85': ('短片', 'shortfilm', ('影视（主分区）', 'cinephile', '181')), '184': ('预告·资讯', 'trailer_info', ('影视（主分区）', 'cinephile', '181')), '181': ('影视（主分区）', 'cinephile', None), '37': ('人文·历史', 'history', ('纪录片（主分区）', 'documentary', '177')), '178': ('科学·探索·自然', 'science', ('纪录片（主分区）', 'documentary', '177')), '179': ('军事', 'military', ('纪录片（主分区）', 'documentary', '177')), '180': ('社会·美食·旅行', 'travel', ('纪录片（主分区）', 'documentary', '177')), '177': ('纪录片（主分区）', 'documentary', None), '147': ('华语电影', 'chinese', ('电影（主分区）', 'movie', '23')), '145': ('欧美电影', 'west', ('电影（主分区）', 'movie', '23')), '146': ('日本电影', 'japan', ('电影（主分区）', 'movie', '23')), '83': ('其他国家', 'movie', ('电影（主分区）', 'movie', '23')), '23': ('电影（主分区）', 'movie', None), '185': ('国产剧', 'mainland', ('电视剧（主分区）', 'tv', '11')), '187': ('海外剧', 'overseas', ('电视剧（主分区）', 'tv', '11')), '11': ('电视剧（主分区）', 'tv', None)}

class Video:
    title = ''
    partition = ''
    type_ = ''
    danmaku = 0
    def __str__(self):
        return "标题：" +self.title + ' 分区' + str(self.partition) + '|' +  str(self.type_)+' 弹幕量：' + str(self.danmaku)

    def __repr__(self):
        return self.__str__()

    def get_list(self):
        return [self.title, self.partition, self.type_, self.danmaku]

def write(video, writer):
    lock.acquire()
    print(video.get_list())
    writer.writerow(video.get_list())
    lock.release()

def read():
    with open("bilibili.csv", "r", encoding="utf-8", errors='ignore', newline="") as f:  
        reader = csv.reader(f)
        data = [row for row in reader]
    return data

# def get_proxy():
#     p_url = ''
#     r = requests.get(p_url)
#     info = json.loads(r.text)
#     print(info)
#     proxy = "http://" + info['data'][0]
#     return {'http':proxy}



def craw_one(id, writer):
    global g_proxies
    aid = str(id)
    path = 'http://api.bilibili.com/x/web-interface/view?aid=' + aid
    resp = requests.get(path, headers=header, proxies=g_proxies)
    resp.close()
    try:
        jt = json.loads(resp.text)
    except:
        return
    #print(g_proxies)
    if jt['code'] == 0:
        if jt['data'] is not None:
            title = jt['data']['title']
            dd = tid_dic[str(jt['data']['tid'])]
            partition = dd[-1]
            type_ = dd[:-1]
            
            danmaku = jt['data']['stat']['danmaku']

            v = Video()
            v.title = title
            v.partition = partition
            v.type_ = type_
            v.danmaku = danmaku
            write(v, writer)
            time.sleep(2)
            return v
    elif jt['code'] == -404:
        print(404)
    elif jt['code'] == -412:
        # 换ip
        exit(-1)
        # g_proxies = get_proxy()
        # craw_one(id)
    else:
        print(jt)

def craw():
    global g_proxies
    videos = list(reversed(range(1,100000001)))
    with open('bilibili.csv','a') as f:
        writer = csv.writer(f)
        while len(videos) != 0:
            tt = []
            for i in range(5):
                t = threading.Thread(target=craw_one, args=(videos.pop(), writer))
                t.start()
                tt.append(t)
            [t.join() for t in tt]
            tt.clear()

def draw():
    dic = {}
    for row in read()[1:]:
        if row[2] not in dic:
            dic[row[2]] = [row, ]
        else:
            dic[row[2]].append(row)
    
    x = []
    y= []
    for key in dic.keys():
        cnt = 0
        for item in dic[key]:
            cnt += int(item[-1])
        x.append(key)
        y.append(cnt)

    li = sorted([z for z in zip(x,y)],key =lambda x: x[-1])
    
    x.clear()
    y.clear()
    for i in li:
        x.append(i[0])
        y.append(i[1])

    pie = Pie("饼图示例")
    pie.add(
        "",
        x,
        y,
        is_label_show=True,
        is_more_utils=True
    )
    pie.render(path="bing.html")

g_proxies = {}
lock = threading.Lock()
if __name__ == '__main__':

    #craw()
    
    draw()