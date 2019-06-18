import time

import requests

from YJS import genrate_proxy
import YJS.data5u as data

__author__ = "Minok"

from scrapy.cmdline import execute

import sys
import os
from YJS.settings import apiUrl

file_path = os.path.dirname(os.path.abspath(__file__))

sys.path.append(file_path)

# 获取IP时间间隔，建议为5秒
# fetchSecond = 300
# # 开始自动获取IP
# genrate_proxy.GetIpThread(apiUrl, fetchSecond).start()

res = requests.get(apiUrl).content.decode()
# 按照\n分割获取到的IP
data.IPPOOL = res.strip().split('\r\n')


time.sleep(3)
execute(["scrapy", "crawl", "yjs"])
