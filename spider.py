# -*- coding: utf-8 -*
import urllib
import re
from bs4 import BeautifulSoup
from lxml import etree
import os
import requests

p = 1
def getbcy(nameid,pageid=1,wrong=0,alltime=0):
    url = u"http://bcy.net/u/%s/post/cos?p=%d" % (nameid,pageid)
    print url
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    headers = {'User-Agent': user_agent, 'Referer': 'http://bcy.net'}
    # html = urllib.urlopen(url,None,headers).read()
    session = requests.session()
    html = session.get(url, headers=headers)
    # page = etree.HTML(html.lower().decode('utf-8'))
    # page=BeautifulSoup(html.text)
    # print page
    soup = BeautifulSoup(html.content, "lxml")
    print soup
    if not os.path.exists("bcy/%s_image" % nameid):
        os.makedirs("bcy/%s_image" % nameid)
    index = 0
    for myimg in soup.find_all('div', class_='postWorkCard__img ovf'):
        img_src = myimg.find('img').get('src')
        img_src = re.sub(r'/tl.*$', "", img_src)
        print img_src
        picname = re.search(r"(?<=/post/).+?(?=$)", img_src, re.M)
        picname = re.search(r"(?<=/).+?(?=$)", picname.group(0), re.M)
        CurrentPath = os.getcwd()
        filename = CurrentPath + "/bcy/%s_image/%s" % (nameid, picname.group(0))
        print picname.group(0)
        try:
            print u'下完了%s张' % (index + 1)
            alltime +=1
            index += 1
            urllib.urlretrieve(url=img_src, filename=filename)
        except Exception:
            print(u'这张图片下载出问题了： %s' % filename)
    pageid += 1
    if index < 12:
        print u'一共下载了 %d 张照片共 %d 页' %(alltime,pageid)
        print u"存储在 %s/bcy/%d_image/" %(CurrentPath, nameid)
        exit(1)
    else:
        getbcy(member_id, pageid, wrong, alltime)

if __name__ == '__main__':
    page = 0
    member_id = raw_input('请输入coser ID，例如：18943,不知道的亲F12在图片的链接里面找')
    getbcy(member_id,page,0,0)
    print "存储在 PY文件目录/CosID 中"
