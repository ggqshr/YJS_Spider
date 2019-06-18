import random

import requests
from scrapy import signals, Request
from scrapy.http import Response
from .settings import apiUrl, lock
from twisted.internet.error import TCPTimedOutError

import YJS.data5u as data


class MyproxiesSpiderMiddleware(object):

    def __init__(self, ip=''):
        self.reset_set = False
        self.bad_ip_set = set()
        self.bad_code_count = 0
        self.ip = ip
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
        thisip = random.choice(data.IPPOOL)
        request.meta["proxy"] = "http://" + thisip
        request.headers['Agent'] = random.choice(self.USER_AGENT_POOL)

    def process_response(self, request, response: Response, spider):
        """
        整体思想是使用锁来控制，但是不能在重置成功后立马释放锁，因为请求队列中还有请求在使用重置ip池之前的ip，
        这些请求在释放了锁之后，也可以进入到if里，从而会出现异常
        现在的办法是使用一个计数器和一个标志位，在重置之后设置一下标志位，现在估计是在将队列中使用之前代理的请求消耗完后
        再释放锁，每一个403请求会让计数减少，而重置完之后的每一次200的请求会让计数器增加，现在是让计数器等于最大线程数的时候释放锁，
        就解决了之前的问题 perfect!
        :param request:
        :param response:
        :param spider:
        :return:
        """
        # 用来输出状态码
        if response.status != 200:
            spider.logger.info(response.status)
        # 如果ip已被封禁，就采取措施
        if response.status == 403:
            # 如果已经重置过ip，在重置ip之前的所有的403请求都会让计数减少
            if self.reset_set:
                self.bad_code_count -= 1
            # 如果ip被封禁，就加入到set中
            self.bad_ip_set.add(request.meta['proxy'])

            # 如果当前set的长度达到和ip池大小相等，且没有加过锁，就重置ip池
            if (len(self.bad_ip_set) == 3 or len(self.bad_ip_set) >= 3) and lock.acquire(blocking=False):
                self.reset_set = True  # 改标记表明已经重置了ip

                # 重置Ip池
                res = requests.get(apiUrl).content.decode()
                # 按照\n分割获取到的IP
                data.IPPOOL = res.strip().split('\r\n')

                # 将被封禁的ipset清空，回复初始状态
                self.bad_ip_set.clear()
                spider.logger.info("reset ip pool!")

            # 如果还有ip可用，将当前的请求换一个代理，重新调度
            thisip = random.choice(data.IPPOOL)
            request.meta['proxy'] = "http://" + thisip
            request.headers['Agent'] = random.choice(self.USER_AGENT_POOL)
            return request
        # 这个状态表明在重置了ip池之后，请求成功的次数，只有达到一定次数，才将锁释放
        if response.status == 200 and self.reset_set:
            # 计数加一
            self.bad_code_count += 1
            if self.bad_code_count == 32:  # 此处的数应该和设置的最大线程数相等，（估计）
                # 回复初试状态
                lock.release()
                self.bad_code_count = 0
                self.reset_set = False

        if response.status == 408:
            self.bad_ip_set.add(request.meta['proxy'])
            thisip = random.choice(data.IPPOOL)
            request.meta['proxy'] = "http://" + thisip
            request.headers['Agent'] = random.choice(self.USER_AGENT_POOL)
            return request
        return response

    def process_exception(self, request, exception, spider):
        if exception is TCPTimedOutError:
            print("time out 啦")
