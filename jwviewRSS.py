# coding:utf-8
from urlresponse import UrlResponse
import os
from infodecrypt import InfoDecrypt
from rssgen import RssGen
from collections import OrderedDict
# from lxml import etree
import datetime

day1 = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime("%m-%d")  # 当天
day2 = (datetime.datetime.utcnow() + datetime.timedelta(hours=8) - datetime.timedelta(days=1)).strftime(
    "%m-%d")  # 昨天

# settings
rsstitle = ["jwview", "中新经纬"]
baseurl = "http://www.jwview.com/"
urlbranch = ["zq.html", "jj.html"]
# 主页的xpath
pathstring = [
    '//ul[@id="news_list"]/li/div[@class="txt"]/h3/a',
]
# 子页的xpath
subpathstring = [
    '//div[contains(@class,"content_zw")]'
]
# 需要删除的xpath
imagedesc = ['//div[@class="title"]', '//div[@class="info borderee"]']
# 是否使用代理
proxied = False

current_dir = os.path.dirname(__file__)  # 当前文件所在目录
xmlpath = os.path.join(current_dir, rsstitle[0] + '.xml')
dbpath = os.path.join(current_dir, 'rss.db')

items = OrderedDict()
for u in urlbranch:
    html = UrlResponse.getresponse(baseurl + u, proxied=proxied)
    # # 二进制byte直接写入文件更好查看是否和浏览器获取的一致，以写入的文件为主
    # html0=etree.HTML(html.decode('GB2312','ignore'),etree.HTMLParser())
    # with open(u[:2]+".html","wb") as f:
    #   f.write(etree.tostring(html0,encoding="utf-8",method = "html"))
    decrypter = InfoDecrypt(dbpath, rsstitle[0], 'gb2312')
    items.update(decrypter.getitems(baseurl, html, pathstring))

itemsall = []
for title, href in items.items():
    # print(title,href)
    if (href.find(day1) + 1) or (href.find(day2) + 1):
        subhtml = UrlResponse.getresponse(href, proxied=proxied)
        # html0=etree.HTML(subhtml.decode('GB2312','ignore'),etree.HTMLParser())
        # with open(u[:2]+".html","wb") as f:
        #   f.write(etree.tostring(html0,encoding="utf-8",method = "html"))
        decrypter.getdetails(title, href, subhtml, subpathstring, imagedesc)

itemsall_list = decrypter.GetAllItems()
if itemsall_list:
    for item in reversed(itemsall_list):
        itemsall.append(RssGen.genitems(item[0], item[2], item[3]))

rss = RssGen.genRss(rsstitle[1], baseurl, rsstitle[1], itemsall)
rss.write_xml(open(xmlpath, "w", encoding='utf-8'),
              encoding='utf-8')  # 生成RSS格式的xml文件
decrypter.DelDBdata()
decrypter.OtherDBControl()