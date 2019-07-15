import logging
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.xlib.pydispatch import dispatcher
import scrapy.spiders

logger = logging.getLogger(__name__)


class SendMail(object):
    def __init__(self):
        dispatcher.connect(self.close, signals.spider_closed)

    def close(self, spider: scrapy.spiders, reason):
        from scrapy.mail import MailSender
        ss = MailSender(
            smtphost='smtp.qq.com',
            mailfrom='942490944@qq.com',
            smtpuser='942490944@qq.com',
            smtppass='ijmbixectujobeei',
            smtpport=465,
            smtpssl=True
        )
        body = f"{spider.name} 已经关闭，原因是{reason},以下是结束的信息\n{spider.crawler.stats._stats}"
        return ss.send(to="942490944@qq.com", subject=f"{spider.name} 爬虫关闭提醒", body=body)
