# coding:utf-8
from lxml import etree
import sqlite3
from pdatabase import DatabaseControl
import datetime, time
from collections import OrderedDict
from urllib import parse
import re


class InfoDecrypt(object):
    """docstring for InfoDecrypt"""
    def __init__(self, dbpath, rsstitle, code='utf-8'):
        self.code = code
        self.dbpath = dbpath
        self.connector = sqlite3.connect(self.dbpath)
        self.db = DatabaseControl(self.connector, rsstitle)
        self.db.CreateTable()
        self.now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)  # 改成北京时间
        self.zerostamp = time.mktime(
            time.strptime(self.now.strftime("%Y-%m-%d 00:00:00"),
                          "%Y-%m-%d %H:%M:%S"))

    def __gethtml(self, htmlres):
        return etree.HTML(htmlres.decode(self.code, 'ignore'),
                          etree.HTMLParser())  # 解析HTML文本内容

    def getitems(self, url, htmlres, pathlist, part=False):
        items = OrderedDict()
        html = self.__gethtml(htmlres)
        contents = html.xpath('|'.join(pathlist))
        if part:  # 注意在使用相对xpath路径时，一定要加‘./’表示当前路径，否则不会得到理想结果
            contents = [content for content in contents if content.xpath(part)]
        contents.reverse()  # 反序排列
        for content in contents:
            title = content.text.strip()
            alldata = self.db.CheckData(title)
            if not alldata:
                href = content.get('href')
                href = parse.urljoin(url, href) if href else parse.urljoin(
                    url,
                    content.xpath('./../@href')[0])  # 取父节点的链接./..
                # print(href)
                items[title] = href
        return items

    def getdetails(self, title, href, subhtml, pathlist, imagedesc=False):
        detile = self.__gethtml(subhtml)
        description = None  # description初始值为None，后面能找到内容则更新
        if detile is not None:
            # time.sleep(1)
            article = detile.xpath('|'.join(pathlist))
            if article:
                if imagedesc:
                    for r in article[0].xpath('|'.join(imagedesc)):
                        r.getparent().remove(r)  # 删除原文中重复的图片说明
                etree.strip_tags(article[0], 'svg', 'path',
                                 'tbody')  # 删除一些标签，tbody必须删，否则表格不显示
                description = etree.tostring(article[0],
                                             encoding="utf-8",
                                             method="html").decode(
                                                 'utf-8')  # 获取含标签的全部内容
                # 调整图片大小
                description = description.replace('width="100%"',
                                                  'width="600"')
                description = description.replace('w=20', 'w=600')
                # 将段落前面开头空两格
                description = re.sub('<p>\\s*', '<p>&emsp;&emsp;', description)
                description = re.sub('<br>\\s*', '<br>&emsp;&emsp;',
                                     description)
            self.db.InsertData(title, self.now.strftime("%Y-%m-%d"), href, description, 
                               self.zerostamp)  # 子网址能打开都记入数据库
        # return description

    def InsertDBdata(self, title):
        self.db.InsertData(title, self.now.strftime("%Y-%m-%d"),
                           self.zerostamp)  # 子网址能打开都记入数据库

    def GetAllItems(self):
        return self.db.GetItems(self.now.strftime("%Y-%m-%d"))

    def DelDBdata(self):
        thirtyday = (self.now -
                     datetime.timedelta(days=30)).strftime("%Y-%m-%d 00:00:00")
        thirtystamp = time.mktime(time.strptime(thirtyday,
                                                "%Y-%m-%d %H:%M:%S"))
        self.db.DelData(thirtystamp)  # 删除数据库30天前的数据

    def OtherDBControl(self):
        self.connector.close()