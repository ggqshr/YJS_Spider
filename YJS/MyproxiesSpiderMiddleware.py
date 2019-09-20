import random

import requests
from proxy_pool.ip_pool import ReachMaxException
from scrapy import signals, Request
from scrapy.http import Response
from twisted.web._newclient import ResponseNeverReceived

from .settings import apiUrl, ip_pool
from twisted.internet.error import TCPTimedOutError, ConnectionRefusedError, TimeoutError, ConnectionLost
from collections import Counter
import YJS.data5u as data


class MyproxiesSpiderMiddleware(object):

    def __init__(self, ip=''):
        self.reset_set = False
        self.bad_ip_set = set()
        self.bad_code_count = 0
        self.ip = ip
        self.timeOutCount = 0
        self.time_out_ip = []
        self.USER_AGENT_POOL = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
            'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
        ]

    def process_request(self, request: Request, spider):
        request.meta["proxy"] = "http://" + ip_pool.get_ip()
        request.headers['Agent'] = random.choice(self.USER_AGENT_POOL)

    def process_response(self, request, response: Response, spider):
        this_res_proxy = request.meta['proxy'].replace("http://", "")
        # 用来输出状态码
        if response.status != 200:
            spider.logger.info(f'{response.status},{response.url}')
        # 如果ip已被封禁，就采取措施
        if response.status == 403:
            ip_pool.report_baned_ip(this_res_proxy)
            thisip = ip_pool.get_ip()
            request.meta['proxy'] = "http://" + thisip
            return request

        if response.status == 408 or response.status == 502 or response.status == 503:
            ip_pool.report_baned_ip(this_res_proxy)
            request.meta['proxy'] = "http://" + ip_pool.get_ip()
            return request
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, ReachMaxException):
            spider.crawler.engine.close_spider(spider, f"reach day max number!!")
            return
        if isinstance(exception,
                      (ConnectionRefusedError, TCPTimedOutError, TimeoutError, ConnectionLost, ResponseNeverReceived)):
            this_bad_ip = request.meta['proxy'].replace("http://", "")
            ip_pool.report_bad_net_ip(this_bad_ip)
        spider.logger.warn(f"{type(exception)} {exception},{request.url}")
        thisip = ip_pool.get_ip()
        request.meta['proxy'] = "http://" + thisip
        return request
