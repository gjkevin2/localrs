# coding:utf-8
from urlresponse import UrlResponse
import os
from infodecrypt import InfoDecrypt
from rssgen import RssGen

# settings
rsstitle = ["thepaper", "澎湃新闻"]
baseurl = "https://www.thepaper.cn"
# 主页的xpath
pathstring = [
    '//div[@id="listContent"]/div/h2/a', '//div[@class="title"]',
    '//ul[@id="listhot0"]/li/a'
]
part = './../following-sibling::div[1]//div[@class="trbstxt"]'  # 只获取部分内容时，用xpath定位，有这部分的才收集
# 子页的xpath
subpathstring = ['//div[@class="news_txt"]', '//div[@id="text_area"]', '//div[contains(@class, "video_main")]']
# 需要删除的图片重复说明xpath
imagedesc = [
    '//p[@class="image_desc"]',
]
# 是否使用代理
proxied = False

current_dir = os.path.dirname(__file__)  # 当前文件所在目录
xmlpath = os.path.join(current_dir, rsstitle[0] + '.xml')
dbpath = os.path.join(current_dir, 'rss.db')

html = UrlResponse.getresponse(baseurl, proxied=proxied)
# 二进制byte直接写入文件更好查看是否和浏览器获取的一致，以写入的文件为主
# from lxml import etree
# html = etree.HTML(html.decode('utf-8', 'ignore'), etree.HTMLParser())
# with open("htmlresult.html", "wb") as f:
#     f.write(etree.tostring(html, encoding="utf-8", method="html"))
decrypter = InfoDecrypt(dbpath, rsstitle[0])
items = decrypter.getitems(baseurl, html, pathstring, part)

itemsall = []
for title, href in items.items():
    # print(title, href)
    # 过滤
    fl = [
        '直播',
    ]
    countsum = sum([title.count(u) for u in fl])
    if countsum: continue
    subhtml = UrlResponse.getresponse(href, proxied=proxied)
    # print(subhtml)
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