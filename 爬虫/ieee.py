import requests
import re
import json
from bs4 import BeautifulSoup
import urllib.parse

requests.packages.urllib3.disable_warnings()

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36', }


class Paper:
    title = ''
    abstract = ''
    refs = []
    link = ''

    def __init__(self, title='', link=''):
        self.title = title
        self.link = link

    def __repr__(self):
        return self.title


def getIeeeAbstarct(id):
    url = r'https://ieeexplore.ieee.org/abstract/document/' + str(id)

    try:
        resp = requests.get(url, timeout=10, verify=False)
    except requests.exceptions.RequestException as e:
        raise e
    html = resp.text
    matchObj = re.findall(r'global.document.metadata=(.*?)};', html, re.M | re.I)
    if len(matchObj) == 1:
        data = matchObj[0] + '}'
        j = json.loads(data)
        abstract = j.get('abstract')  # 提取摘要
        return abstract
    return ''


def getIeeeAbstarctByUrl(url):
    try:
        resp = requests.get(url, timeout=10, verify=False)
    except requests.exceptions.RequestException as e:
        raise e
    html = resp.text
    matchObj = re.findall(r'global.document.metadata=(.*?)};', html, re.M | re.I)
    if len(matchObj) == 1:
        data = matchObj[0] + '}'
        j = json.loads(data)
        abstract = j.get('abstract')  # 提取摘要
        return abstract
    return ''


def getbiomedcentralAbstract(html):
    matchObj = re.findall(r'"og:description" content="(.*?)"/>', html, re.M | re.I)
    if len(matchObj) == 1:
        abstract = matchObj[0]  # 提取摘要
        return abstract
    return ''


def getWileyAbstract(html):
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('div', class_='article-section__content en main')

    if res:
        abstract = res.p.string  # 提取摘要
        return abstract
    return ''


def getSciencedirect(url):
    try:
        resp = requests.get(url, headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'referer': url
    })
    except requests.exceptions.RequestException as e:
        raise e
    resp.encoding = 'utf8'
    html = resp.text
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('div', class_='abstract author')

    if res:
        abstract = res.div.p.text  # 提取摘要
        return abstract
    return ''


def getatlantis_pressAbstract(html):
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('div', class_='src-components-content textContent')

    if res:
        abstract = res.string  # 提取摘要
        return abstract
    return ''


def getAcmAbstract(html):
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('div', class_='abstractSection abstractInFull')

    if res:
        abstract = res.p.text  # 提取摘要
        return abstract
    return ''


def getGoogleScholar(html):
    return ''


def getSpringerChapterAbstract(html):
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('p', class_='Para')

    if res:
        abstract = res.string  # 提取摘要
        return abstract
    return ''


def getSpringerArticleAbstract(html):
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('div', class_='c-article-section__content')

    if res:
        abstract = res.p.string  # 提取摘要
        return abstract
    return ''


def getSpringerNatureAbstract(html):
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('div', class_='c-article-section__content')

    if res:
        abstract = res.p.string  # 提取摘要
        return abstract
    return ''


def getSpringerOpenArticleAbstract(html):
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('div', class_='c-article-section__content')

    if res:
        abstract = res.p.string  # 提取摘要
        return abstract
    return ''


def getSagepubAbstract(html):
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('div', class_='abstractSection abstractInFull')

    if res:
        abstract = res.p.string  # 提取摘要
        return abstract
    return ''


def getMdpiAbstract(html):
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('div', class_='art-abstract in-tab hypothesis_container')
    if res:
        abstract = res.text  # 提取摘要
        return abstract
    return ''


def getArxivAbstract(html):
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('blockquote', class_='abstract mathjax')

    if res:
        abstract = res.string  # 提取摘要
        return abstract
    return ''


def getResearchgateAbstract(html):
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('div',
                    class_='nova-e-text nova-e-text--size-m nova-e-text--family-sans-serif nova-e-text--spacing-auto nova-e-text--color-inherit')

    if res:
        abstract = res.text  # 提取摘要
        return abstract
    return ''


def getNipsAbstract(html):
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('p', class_='abstract')

    if res:
        abstract = res.string  # 提取摘要
        return abstract
    return ''


def getNcbiPubmedAbstract(html):
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('div', class_='abstract-content selected')

    if res:
        abstract = res.p.string  # 提取摘要
        return abstract
    return ''

def getNcbiPmcAbstract(html):
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('p', class_='p p-first-last')

    if res:
        abstract = res.string  # 提取摘要
        return abstract
    return ''


def getAbstract(url):
    if url.find('ieeexplore.ieee.org') != -1:
        return getIeeeAbstarctByUrl(url)

    if url.find('scholar.google') != -1:
        return ''

    try:
        resp = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        raise e

    fhtml = resp.text

    last_url = url
    if len(resp.history) > 1:
        last_url = resp.history[-1].headers['location']

    try:
        resp = requests.get(last_url, headers=headers)
    except requests.exceptions.RequestException as e:
        raise e
    resp.encoding = 'utf8'
    html = resp.text

    if last_url.find('elsevier.com') != -1:
        soup = BeautifulSoup(html, 'lxml')
        res = soup.find('input', id='redirectURL')
        if res:
            url = res['value']
            url = urllib.parse.unquote(url)
        return getAbstract(url)

    if last_url.find('ieeexplore.ieee.org') != -1 or html.find("IEEE Xplore, delivering full text access to the world's highest quality technical literature in engineering and technology") != -1:
        return getIeeeAbstarctByUrl(last_url)

    if last_url.find('sciencedirect.com') != -1 or html.find('S1878535217300990') != -1:
        return getSciencedirect(last_url)

    if last_url.find('biomedcentral.com') != -1 or html.find('biomedcentral.com') != -1:
        return getbiomedcentralAbstract(html)

    if last_url.find('springer.com/book') != -1 or html.find('springer.com/book') != -1:
        return 'drop'

    if last_url.find('springeropen.com/articles') != -1 or html.find('springeropen.com/articles') != -1:
        return getSpringerOpenArticleAbstract(html)

    if last_url.find('onlinelibrary.wiley.com') != -1 or html.find('onlinelibrary.wiley.com') != -1:
        return getWileyAbstract(html)

    if last_url.find('www.atlantis-press.com') != -1 or html.find('www.atlantis-press.com') != -1:
        return getatlantis_pressAbstract(html)

    if last_url.find('dl.acm.org') != -1 or html.find('dl.acm.org') != -1:
        return getAcmAbstract(html)

    if last_url.find('springer.com/chapter') != -1 or html.find('springer.com/chapter') != -1:
        return getSpringerChapterAbstract(html)

    if last_url.find('springer.com/article') != -1 or html.find('springer.com/article') != -1:
        return getSpringerArticleAbstract(html)

    if last_url.find('nature.com') != -1 or html.find('nature.com') != -1:
        return getSpringerNatureAbstract(html)

    if last_url.find('journals.sagepub.com') != -1 or html.find('journals.sagepub.com') != -1:
        return getSagepubAbstract(html)

    if last_url.find('ncbi.nlm.nih.gov/pubmed') != -1 or html.find('http://updates.html5rocks.com/2014/11/Support-for-theme-color-in-Chrome-39-for-Android') != -1:
        return getNcbiPubmedAbstract(html)

    if last_url.find('ncbi.nlm.nih.gov/pmc') != -1 or html.find('ncbi_pcid') != -1:
        return getNcbiPmcAbstract(html)

    if last_url.find('mdpi.com') != -1 or html.find('mdpi.com') != -1:
        return getMdpiAbstract(html)
    if last_url.find('nips.cc') != -1 or html.find('nips.cc') != -1:
        return getNipsAbstract(html)

    if last_url.find('arxiv.org') != -1 or html.find('arxiv.org') != -1:
        return getArxivAbstract(html)

    if last_url.find('researchgate.net') != -1 or html.find('researchgate.net') != -1:
        return getResearchgateAbstract(html)

    if url.find('scholar.google') != -1 or html.find('scholar.google') != -1:
        return getGoogleScholar(html)
    return ''


# https://dl.acm.org/doi/10.1016/j.patcog.2014.10.012


def getRefUrlAcm(url):
    papers = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    }
    try:
        resp = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        raise e
    html = resp.text
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('ol', class_='references__list')
    res = res.find_all('li', class_='references__item')
    for item in res:
        note = item.find('span', class_='references__note')
        title = note.text.replace('\n',' ')
        suffix = note.find_all('span', class_='references__suffix')
        # for item in suffix:
        url = suffix[-1].a['href']
        if url.startswith('/servlet'):
            url = "https://dl.acm.org" + url
        # try:
        #     resp = requests.get(url, headers=headers)
        # except requests.exceptions.RequestException as e:
        #     raise e
        #
        # url = urllib.parse.unquote(resp.history[-1].headers['location'])
        # if url.find('scholar.google.com') != -1:
        #     url = url.split('&hl=en&q')[0].split('http://www.google.com/sorry/index?continue=')[1]
        # print(url)
        p = Paper()
        p.title = title
        p.link = url
        papers.append(p)
    return papers



def getRefUrlNcbi(url):
    papers = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    }
    try:
        resp = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        raise e
    html = resp.text
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find_all('div', class_='ref-cit-blk half_rhythm')

    for item in res:
        note = item.find('span', class_='element-citation')
        rlink = str(note)

        match = re.findall(r'href=[\'"]?([^\'" >]+)', rlink)

        def fun(link):
            url = urllib.parse.unquote(link)
            url = url.replace('&amp;', '&')
            if url.startswith('/pubmed') or url.startswith('/pmc'):
                url = 'https://www.ncbi.nlm.nih.gov' + url
            elif url.startswith('//dx'):
                url = "http:" + url
            return url
        url = list(map(fun, match))[0]

        title = note.text
        p = Paper()
        p.title = title
        p.link = url
        papers.append(p)
    return papers


def getRefUrlSpring(url):
    papers = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    }
    try:
        resp = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        raise e
    html = resp.text
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find_all('li', class_='c-article-references__item')

    for item in res:
        title = item.p.text
        print(title)

        rlink = str(item)
        match = re.findall(r'href=[\'"]?([^\'" >]+)', rlink)

        def fun(link):
            url = urllib.parse.unquote(link)
            url = url.replace('&amp;', '&')
            if url.startswith('/pubmed') or url.startswith('/pmc'):
                url = 'https://www.ncbi.nlm.nih.gov' + url
            elif url.startswith('//dx'):
                url = "http:" + url
            return url
        l = list(map(fun, match))
        url = ''
        if len(l) > 0:
            url = list(map(fun, match))[0]

        p = Paper()
        p.title = title
        p.link = url
        papers.append(p)
    return papers


def getRefUrl(id):
    url = 'https://ieeexplore.ieee.org/rest/document/' + str(id) + '/references'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'Referer': r'https://ieeexplore.ieee.org/abstract/document/' + str(id), 'Host': 'ieeexplore.ieee.org'}
    try:
        resp = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        raise e
    html = resp.text
    j = json.loads(html)

    references = j['references']
    refs = []

    for item in references:
        p = Paper()
        if 'title' in item:
            p.title = item['title']
        elif 'text' in item:
            p.title = item['text']
        else:
            raise ValueError()
        if 'links' in item:
            if 'documentLink' in item['links']:
                p.link = 'https://ieeexplore.ieee.org/abstract' + item['links']['documentLink']
            elif 'crossRefLink' in item['links']:
                p.link = item['links']['crossRefLink']
            elif 'acmLink' in item['links']:
                p.link = item['links']['acmLink']
            else:
                if 'googleScholarLink' in item:
                    p.link = item['googleScholarLink']
        elif 'googleScholarLink' in item:
            p.link = item['googleScholarLink']
        else:
            pass
        refs.append(p)
    return refs


def getAbstractOne(ref, f):
    error = False

    try:
        print("开始处理：", ref.link)
        t = getAbstract(ref.link)
        if t:
            ref.abstract = t.strip()

        if ref.abstract and ref.abstract == '':
            print("--处理失败", ref.link)
            f.write("title: " + ref.title)
            f.write('\n')
            f.write("url: " + ref.link)
            f.write('\n')
            f.write("abstract: " + ref.abstract)
            f.write('\n\n')
            error = True
        else:
            print("成功：", ref.title)
            f.write("title: " + ref.title)
            f.write('\n')
            if ref.abstract:
                f.write("abstract: " + ref.abstract)
            else:
                f.write("url: " + ref.link)
                f.write('\n')
                f.write("abstract: ")
            f.write('\n\n')
            error = False

    except requests.exceptions.RequestException as e:
        f.write("title: " + ref.title)
        f.write('\n')
        f.write("url: " + ref.link)
        f.write('\n')
        f.write("abstract: " + ref.abstract)
        f.write('\n\n')
        error = False
        print(e, ref.link)
    if error:
        return ref
    else:
        return None


def getAllAbstract(refs, f):
    errors = []
    for ref in refs:
        if getAbstractOne(ref, f):
            errors.append(ref)

    return errors


def testIeee(ieeeid):
    abstact = getIeeeAbstarct(ieeeid)
    refs = getRefUrl(ieeeid)

    f = open('log' + str(ieeeid), 'a')

    errors = getAllAbstract(refs, f)
    print(errors)


def testAcm():
    url = "https://dl.acm.org/doi/10.1016/j.patcog.2014.10.012"
    refs = getRefUrlAcm(url)

    f = open('log'+url[-5:], 'a')

    errors = getAllAbstract(refs, f)
# https://scholar.google.com/scholar_lookup?journal=Proceedings+of+the+2015+IEEE+International+Conference+on+Image+Processing+(ICIP)&title=Utd-mhad:+A+multimodal+dataset+for+human+action+recognition+utilizing+a+depth+camera+and+a+wearable+inertial+sensor&author=C.+Chen&author=R.+Jafari&author=N.+Kehtarnavaz&pages=168-172&
# https://scholar.google.com/scholar_lookup?journal=IEEE+Multimed.&title=Microsoft+kinect+sensor+and+its+effect&author=Z.+Zhang&volume=19&publication_year=2012&pages=4-10&doi=10.1109/MMUL.2012.24&
def testNcbi():
    url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6427427"
    refs = getRefUrlNcbi(url)

    f = open('log'+url[-5:], 'a')

    errors = getAllAbstract(refs, f)

def testSpring():
    url = 'https://link.springer.com/article/10.1007/s11042-015-3177-1'
    refs = getRefUrlSpring(url)

    f = open('log'+url[-5:], 'a')

    errors = getAllAbstract(refs, f)

if __name__ == '__main__':
    testSpring()