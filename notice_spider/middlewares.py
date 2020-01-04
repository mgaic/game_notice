# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import random
import re
from scrapy import signals
import redis
import json
from fake_useragent import UserAgent

class NoticeSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class NoticeSpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    def __init__(self):
        self.conn = redis.Redis(host='192.168.1.21', port=6379, db=8)

    def process_request(self, request, spider):
        if request.url.startswith("http://"):
            proxy = self.get_proxy_by_redis()['proxy']['http']

            # no_auth_proxy = proxy.replace(re.findall('http://(.*)@', proxy)[0], '').replace('@', '')
            # print('no_auth_proxy', no_auth_proxy)
            request.meta['proxy'] = proxy     # http代理\

            # proxy_user_pass = re.findall('http://(.*)@', proxy)[0]
            # print('proxy_user_pass',proxy_user_pass)
            # encoded_user_pass = base64.b64encode(proxy_user_pass.encode("utf-8"))
            # request.headers['Proxy-Authorization'] = 'Basic' + str(encoded_user_pass, encoding='utf-8')
            print('代理中间件: {}'.format(request.meta['proxy']))
            # return request
        elif request.url.startswith("https://"):
            proxy = self.get_proxy_by_redis()['proxy']['https']
            # no_auth_proxy = proxy.replace(re.findall('https://(.*)@', proxy)[0], '').replace('@', '')
            # print('no_auth_proxy', no_auth_proxy)
            request.meta['proxy'] = proxy  # http代理\

            # proxy_user_pass = re.findall('https://(.*)@', proxy)[0]
            # print('proxy_user_pass', proxy_user_pass)
            # encoded_user_pass = base64.b64encode(proxy_user_pass.encode("utf-8"))
            # request.headers['Proxy-Authorization'] = 'Basic' + str(encoded_user_pass, encoding='utf-8')
            print('代理中间件: {}'.format(proxy))
            # return request

    # def process_response(self, request, response, spider):
    #     '''对返回的response处理'''
    #     # 如果返回的response状态不是200，重新生成当前request对象
    #     if response.status != 200:
    #         if request.url.startswith("http://"):
    #             request.meta['proxy'] = self.get_proxy_by_redis()['proxy']['http']  # http代理
    #         elif request.url.startswith("https://"):
    #             request.meta['proxy'] = self.get_proxy_by_redis()['proxy']['https']
    #         print('process_response')
    #         return request
    #     return response

    def process_exception(self, request, exception, spider):
        # 出现异常时（超时）使用代理
        if request.url.startswith("http://"):
            request.meta['proxy'] = self.get_proxy_by_redis()['proxy']['http']  # http代理
        elif request.url.startswith("https://"):
            request.meta['proxy'] = self.get_proxy_by_redis()['proxy']['https']  # https代理
        print("process_exception")
        print(request.headers)
        return request

    def get_proxy_by_redis(self, key='AG_Proxy_Seabright_广州市'):
        # 获取供应商IP
        proxies = self.conn.get(key).decode()
        if isinstance(proxies, str):
            proxies = json.loads(proxies)
        results = []
        for proxy in proxies:
            if isinstance(proxy, str):
                proxy = json.loads(proxy)
            proxy_info = {
                "http": "http://%s" % proxy.get('ip'),
                "https": "http://%s" % proxy.get('ip')
            }
            results.append({
                'proxy': proxy_info
            })
        proxy = random.choice(results)
        return proxy

class RandomUserAgentMiddleware(object):

    def process_request(self, request, spider):
        ua = UserAgent()
        request.headers['User-Agent'] = ua.random
