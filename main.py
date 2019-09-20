import time

import requests

from YJS import genrate_proxy
import YJS.data5u as data
from YJS.settings import ip_pool

__author__ = "Minok"

from scrapy.cmdline import execute


ip_pool.start()

execute(["scrapy", "crawl", "yjs"])
