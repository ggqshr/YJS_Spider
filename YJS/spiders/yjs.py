# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List

import scrapy
from scrapy.http import Request
from urllib import parse
import time
from YJS.items import YjsItemLoader, YjsOtherItem, YjsSelfItem, YjsItem
import pysnooper
import locale
import random
from urllib.parse import quote

locale.setlocale(locale.LC_CTYPE, 'chinese')


class YjsSpider(scrapy.Spider):
    name = 'yjs'
    allowed_domains = ['yingjiesheng.com']
    industry_list = ['互联网·电商', '网络游戏', '计算机软件', 'IT服务', '电子', '通信工程', '计算机硬件', '建筑工程', '规划设计', '房地产服务', '银行', '保险',
                     '投资', '会计/审计', '信托/担保/拍卖/典当', '快消品', '批发零售', '服装服饰', '家电业', '办公设备', '奢侈品收藏品', '工艺品珠宝玩具', '汽车·摩托车',
                     '机械制造', '印刷·包装·造纸', '原材料加工', '工业自动化', '生物制药工程', '医疗保健·美容', '医疗器械', '能源·水利', '化工行业', '采掘·冶炼',
                     '环保行业', '新能源', '专业咨询', '中介服务', '外包服务', '检测认证', '旅游酒店餐饮', '娱乐休闲', '租赁服务', '广告会展', '影视文化', '教育培训',
                     '运输物流', '进出口贸易', '航空航天', '政府机构', '农林牧渔', '其他行业']
    start_url = [
        'http://s.yingjiesheng.com/search.php?word=&area=1999&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=1349&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=1056&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=1085&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=1102&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=1186&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=1217&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=1376&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=1352&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2105&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2106&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2102&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2103&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2104&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2108&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2109&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2111&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2136&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2113&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2116&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2115&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2118&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2119&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2120&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2121&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2127&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2130&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2138&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2139&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2134&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2101&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2100&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2107&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2110&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2112&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2114&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2131&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2132&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2142&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2117&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2122&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2123&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2128&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2126&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2129&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2137&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2140&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2141&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2133&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2143&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2144&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2135&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2124&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2125&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=&area=2144&jobterm=0&do=1&stype=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=%E5%BC%80%E5%8F%91+-%E5%9C%B0%E4%BA%A7+-%E9%94%80%E5%94%AE+%E6%A0%A1%E6%8B%9B&start=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=%E5%BC%80%E5%8F%91+-%E5%9C%B0%E4%BA%A7+-%E9%94%80%E5%94%AE+%E6%A0%A1%E5%9B%AD%E6%8B%9B%E8%81%98&start=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=%E7%A0%94%E5%8F%91+-%E5%9C%B0%E4%BA%A7+-%E9%94%80%E5%94%AE+%E6%A0%A1%E6%8B%9B&start=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=%E7%A0%94%E5%8F%91+-%E5%9C%B0%E4%BA%A7+-%E9%94%80%E5%94%AE+%E6%A0%A1%E5%9B%AD%E6%8B%9B%E8%81%98&start=0&sort=date&period=4',
        'http://s.yingjiesheng.com/search.php?word=%E5%BC%80%E5%8F%91+-%E5%9C%B0%E4%BA%A7+-%E9%94%80%E5%94%AE&area=0&sort=date&period=4',
    ]

    def start_requests(self):
        for industry in self.industry_list:
            self.start_url.append(f"http://s.yingjiesheng.com/search.php?word={quote(industry)}&sort=date&period=4")
        for page in self.start_url:
            yield Request(
                url=page,
            )

    # 列表页数据获取
    def parse(self, response):

        import re

        """

        1.获取列表url，交给scrapy下载后进行详情解析
        2。获取下一页url交给scrapy进行下载，下载完后交给parse提取url

        """
        # 获取数据部分
        post_part = response.xpath("//ul[contains(@class,'searchResult')]/li")
        if len(post_part) == 0:
            yield None
        for post_node in post_part:
            # 标题
            title_selector = post_node.xpath("div/h3/a")
            title = title_selector.xpath('string(.)').extract_first('')
            # 信息来源
            tag_original = post_node.xpath("div/p/text()").extract_first('')
            tag_deal = tag_original.replace(' ', '').replace('\r\n', '')
            tag_obj = re.match(".*?\：(.*)", tag_deal)
            if tag_obj:
                tag = tag_obj.group(1)
            else:
                tag = ""
            # 查找标签是否有本站 没有type值为 -1
            type = 1 if tag.find("本站") != -1 else 0
            # 页面链接
            post_url = post_node.xpath("div/h3/a/@href").extract_first()
            # 抓取详情数据
            if title != "":
                if type:
                    yield Request(url=parse.urljoin(response.url, post_url),
                                  meta={"title": title, "tag": tag, "type": type, 'dont_retry': True},
                                  callback=self.pars_self)
                else:
                    yield Request(url=parse.urljoin(response.url, post_url),
                                  meta={"title": title, "tag": tag, "type": type, 'dont_retry': True},
                                  callback=self.pars_other)

            # 变量初始化
            title_selector = ''
            source_original = ''

        next_url = response.xpath("//div[contains(@class,'page')]/a[text()='下一页']/@href").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    # 其他网站数据详情获取
    def pars_other(self, response):

        item_loader = YjsItemLoader(item=YjsItem(), response=response)
        item_loader.add_value("job_name", response.meta.get("title", ""))
        item_loader.add_value("link", response.url)
        tag = response.meta.get("tag", "")
        item_loader.add_value("place", tag.split("|")[-1] if tag != "" else "空")
        item_loader.add_xpath("company_name", "//div[contains(@class,'mleft')]/h1/text()")
        item_loader.add_xpath("post_time", "//div[contains(@class,'info clearfix')]/ol/li[text()='发布时间：']/u/text()")
        item_loader.add_xpath("job_nature", "//div[contains(@class,'info clearfix')]/ol/li[text()='职位类型：']/u/text()")
        item_loader.add_xpath("job_place", "//div[contains(@class,'info clearfix')]/ol/li[text()='工作地点：']/u/text()")
        item_loader.add_value("job_content",
                              response.xpath("//div[contains(@class,'job')]").xpath("string(.)").extract_first(""))
        item_loader.add_xpath("job_name", "//div[contains(@class,'info clearfix')]/ol/li[text()='职位：']/u/text()")
        post_time = item_loader.get_output_value("post_time") if item_loader.get_output_value(
            "post_time") is not None else time.ctime()
        company_name = item_loader.get_output_value("company_name")
        try:
            item_loader.add_value("id",
                                  company_name if company_name is not None else "空" + item_loader.get_output_value(
                                      "job_name") + post_time)
        except TypeError:
            item_loader.add_value("id", random.random())
        yjs_other_item = item_loader.load_item()
        # 将没有字段设置默认值
        for f in yjs_other_item.fields.keys():
            if f not in dict(yjs_other_item):
                yjs_other_item.setdefault(f, "空")
        yield yjs_other_item

    # 本站数据详情获取
    def pars_self(self, response):

        company_intro_obj = response.xpath("//div[contains(@class,'main')]/div[4]/p")
        company_intro = ''
        for intro_node in company_intro_obj:
            company_intro += intro_node.xpath("text()").extract_first()

        location_obj = response.xpath(
            "//div[contains(@class,'main')]/div[2]/div[contains(@class,'job_list')]/ul/li[1]/span")
        location = str(location_obj.xpath("a/text()").extract_first() if location_obj.xpath(
            "a/text()").extract_first() else location_obj.xpath("text()").extract_first())

        item_loader = YjsItemLoader(item=YjsItem(), response=response)
        item_loader.add_value("job_name", response.meta.get("title", ""))
        item_loader.add_value("link", response.url)
        tag = response.meta.get("tag", "")
        item_loader.add_value("place", tag.split("|")[-1] if tag != "" else "空")
        item_loader.add_xpath("company_name", "//div[contains(@class,'main')]/div[1]/h1/a/text()")
        item_loader.add_xpath("company_industry", "//div[contains(@class,'main')]/div[1]/ul/li[1]/span/text()")
        item_loader.add_xpath("company_size", "//div[contains(@class,'main')]/div[1]/ul/li[2]/span/text()")
        item_loader.add_xpath("company_nature", "//div[contains(@class,'main')]/div[1]/ul/li[3]/span/text()")
        item_loader.add_value("job_name", response.xpath("//div[contains(@class,'main')]/div[2]/h2").xpath(
            "string(.)").extract_first())
        item_loader.add_value("job_place", location)
        valid_date = response.xpath(
            "//div[contains(@class,'main')]/div[2]/div[contains(@class,'job_list')]/ul/li[2]/span/text()").extract_first()
        timeformat = time.strptime(valid_date.split("至")[-2].strip(), "%Y年%m月%d日") if valid_date is not None else "空"
        item_loader.add_value("post_time",
                              time.strftime("%Y-%m-%d",
                                            timeformat) if valid_date is not None else datetime.now().strftime(
                                  "%Y-%m-%d"))
        item_loader.add_xpath("job_number",
                              "//div[contains(@class,'main')]/div[2]/div[contains(@class,'job_list')]/ul/li[3]/span/text()")
        item_loader.add_xpath("job_nature",
                              "//div[contains(@class,'main')]/div[2]/div[contains(@class,'job_list')]/ul/li[4]/text()")
        item_loader.add_value("job_content", response.xpath(
            "//div[contains(@class,'main')]/div[2]/div[contains(@class,'job_list')]/div[contains(@class,'j_i')]").xpath(
            "string(.)").extract_first())
        item_loader.add_value("company_intro", company_intro)
        item_loader.add_xpath("company_homepage", "//div[contains(@class,'main')]/div[4]/ul/li/a/text()")
        try:
            item_loader.add_value("id", item_loader.get_output_value("company_name") + item_loader.get_output_value(
                "job_name") + item_loader.get_output_value("post_time"))
        except TypeError:
            item_loader.add_value("id", str(random.random()))
        yjs_self_item = item_loader.load_item()
        yield yjs_self_item
