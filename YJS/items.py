# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from datetime import datetime
from typing import List

import scrapy
from YJS.helper import md5
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Compose, Join
import base64

regSpace = re.compile(r'([\s\r\n\t])+')


def GetMd5(value):
    return md5(value)


def encodeBase(s):
    return base64.b32encode(s.encode("utf-8")).decode("utf-8")


def replace_all_n(text):
    # 以防止提取不到
    try:
        if type(text) == str:
            rel = re.sub(regSpace, "", text)
            return rel
        elif type(text) == list:
            return "".join([re.sub(regSpace, "", t) for t in text])
    except TypeError as e:
        return "空"


# 他妹的，这人数居然还有"多人"这个写法！
def GetRecruitNum(value):
    num_obj = re.match("([\d]*).*", value)
    if num_obj:
        return str(num_obj.group(1))
    else:
        num_obj = re.match("([\u4e00-\u9fa5]*).*", value)
        return num_obj.group(1)


def GetPositionType(value):
    position_type_obj = re.match("职位性质：(.*)", value)
    position_type = position_type_obj.group(1) if position_type_obj else "未知"
    return position_type


def RemoveBlankCharacter(value):
    return value.replace("\r\n", "").replace("\t", "")


def parse(s, loader_context):
    if s is List:
        return s if len(s) != 0 else ["空"]
    elif s is str:
        return [s] if len(s) != 0 else ["空"]
    # return s if len(s) != 0 else ["空"]


def t_past(x):
    if x is None:
        return "空"
    return x


def process_time(x):
    if len(x) == 0:
        return [datetime.now().strftime("%Y-%m-%d")]
    if x is str:
        return [x]
    return x


class YjsItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = Compose(TakeFirst(), t_past)


class YjsSelfItem(scrapy.Item):
    type = scrapy.Field()
    url = scrapy.Field()
    url_md5 = scrapy.Field(input_processor=MapCompose(GetMd5), )
    title = scrapy.Field()
    tag = scrapy.Field()
    company = scrapy.Field()
    industry = scrapy.Field()
    company_size = scrapy.Field()
    company_type = scrapy.Field()
    position_title = scrapy.Field()
    location = scrapy.Field()
    recruit_num = scrapy.Field(input_processor=MapCompose(GetRecruitNum), )
    position_type = scrapy.Field(input_processor=MapCompose(GetPositionType), )
    position_desc = scrapy.Field(input_processor=MapCompose(RemoveBlankCharacter), )
    company_intro = scrapy.Field(input_processor=MapCompose(RemoveBlankCharacter), )
    company_site = scrapy.Field()
    created_at = scrapy.Field()
    valid_date = scrapy.Field()


class YjsOtherItem(scrapy.Item):
    type = scrapy.Field()
    url = scrapy.Field()
    url_md5 = scrapy.Field(
        input_processor=MapCompose(GetMd5),
    )
    title = scrapy.Field()
    tag = scrapy.Field()
    company = scrapy.Field()
    post_date = scrapy.Field()
    location = scrapy.Field()
    position_title = scrapy.Field()
    position_type = scrapy.Field()
    source = scrapy.Field()
    major_label = scrapy.Field()
    content = scrapy.Field(input_processor=MapCompose(RemoveBlankCharacter))
    created_at = scrapy.Field()


class YjsItem(scrapy.Item):
    id = scrapy.Field(input_processor=MapCompose(encodeBase))  # 根据公司名工作名和发布时间生成
    link = scrapy.Field()
    job_name = scrapy.Field(input_processor=Join())
    company_name = scrapy.Field()
    post_time = scrapy.Field(output_processor=Compose(process_time, TakeFirst()))
    job_place = scrapy.Field()
    job_nature = scrapy.Field()
    job_content = scrapy.Field(input_processor=MapCompose(replace_all_n))
    company_homepage = scrapy.Field()
    company_size = scrapy.Field()
    company_nature = scrapy.Field()
    company_industry = scrapy.Field()
    job_number = scrapy.Field(input_processor=MapCompose(replace_all_n))
    place = scrapy.Field(input_processor=MapCompose(replace_all_n))
    company_intro = scrapy.Field(input_processor=MapCompose(replace_all_n))
