# -*- coding: utf-8 -*-

# Scrapy settings for YJS project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
from logging import INFO

BOT_NAME = 'YJS'

SPIDER_MODULES = ['YJS.spiders']
NEWSPIDER_MODULE = 'YJS.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'YJS (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'YJS.middlewares.YjsSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'YJS.middlewares.YjsSpiderMiddleware': 543,
    "YJS.MyproxiesSpiderMiddleware.MyproxiesSpiderMiddleware": 125
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'YJS.pipelines.YjsPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 用来直接将item导出的
# FEED_FORMAT = "csv"
#
# FEED_URI='./test.csv'

LOG_LEVEL = INFO

from scrapy.utils.log import configure_logging
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os

if not os.path.exists("./logs"):
    os.mkdir('./logs')

configure_logging(install_root_handler=False)
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        RotatingFileHandler(filename='logs/Liepin{}.log'.format(datetime.now().strftime("%Y.%m.%d")), encoding='utf-8')]
)

REDIS_HOST = "116.56.140.202"
REDIS_PORT = 6379

MODE = "LOCAL"  # or YAO

MONGODB_HOST = "116.56.140.202"
MONGODB_PORT = 27017

apiUrl = "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=d460f14ed5ae426e8a7164005c61b9e7&orderno=YZ20196121637TQppQw&returnType=1&count=3"

from threading import Lock

lock = Lock()
