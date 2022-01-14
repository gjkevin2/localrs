# coding:utf-8
import urllib.request, urllib.parse
from urllib.error import URLError
import ssl

ssl._create_default_https_context = ssl._create_unverified_context  # 取消全局认证
import socket

socket.setdefaulttimeout(30)  # 设置socket层的超时时间30秒


class UrlResponse(object):
    """use get/post method to get information"""
    # 请求头，有些页面需要登录后才能抓取，cookie长期有效的可以设置cookie
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }

    @classmethod
    def __proxyset(cls):
        # proxy=urllib.request.ProxyHandler({'http':"http://127.0.0.1:7071","https":"https://127.0.0.1:7071"}) # 使用urllib.request.ProxyHandler()设置代理服务器信息
        # opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler) # 创建全局默认opener对象使urlopen()使用opener
        # urllib.request.install_opener(opener)
        import socks
        socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 10808)
        socket.socket = socks.socksocket

    @classmethod
    def getresponse(cls,
                    htmlsource,
                    headers=None,
                    method="GET",
                    data=None,
                    proxied=False):
        if headers is None: headers = cls.headers  # 使用默认值-类变量
        if proxied:
            cls.__proxyset()  # 类方法只能调用类方法，因为其他方法需要实例化
        if method == "POST":
            if isinstance(data, dict):
                data = urllib.parse.urlencode(data).encode('utf-8')
            # request=urllib.request.Request(htmlsource,headers=cls.headers,data=data)
        # else:
        request = urllib.request.Request(htmlsource, headers=headers)
        try:
            response = urllib.request.urlopen(request, data=data)  # timeout防止时间长造成假死
        # except HTTPError as e:
        #     print(e.code,e.reason,sep='\n')
        #     return None
        except URLError as e:
            print(e.reason)
            # if isinstance(e.reason,socket.timeout):
            #     print("超时")
            return None
        try:
            html = response.read()
            response.close()  # 关闭response避免被封
            return html
        except ssl.SSLError as err:
            print(err)
            response.close()  # 关闭response避免被封
            return None