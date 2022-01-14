# coding:utf-8
import datetime
import PyRSS2Gen


class RssGen(object):
    """docstring for RssGen"""
    utcnow = datetime.datetime.utcnow()  # 国内是+8区，美国是-5区

    @classmethod
    def genitems(cls, title, href, descriptions, pubDate=''):
        item = PyRSS2Gen.RSSItem(  # item即为一项内容
            title=title,  # 每一项内容的标题
            link=href,  # 每一项内容的链接
            description=descriptions,  # 每一项内容的描述/内容
            pubDate=cls.utcnow if not pubDate else pubDate  # 更新时间,默认采用GMT时间
        )
        return item

    @classmethod
    def genRss(cls, title, link, description, rssitems):
        rss = PyRSS2Gen.RSS2(
            title=title,  # rss源的名称
            link=link,  # rss源的原地址
            description=description,  # rss源的描述
            lastBuildDate=cls.utcnow,  
            items=rssitems)
        return rss