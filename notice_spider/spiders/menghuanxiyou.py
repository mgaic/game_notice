# -*- coding: utf-8 -*-
import hashlib
import json
import random
import time
import scrapy
from notice_spider.items import NoticeSpiderItem
import redis


class MenghuanxiyouSpider(scrapy.Spider):
    name = 'MenghuanxiyouSpider'

    def __init__(self, *args, **wkargs):
        super().__init__(**wkargs)
        self.activity_page = 1
        self.news_page = 1
        self.notice_page = 1
        self.new_server_page = 1
        self.conn = redis.Redis(host='192.168.1.21', port=6379, db=8)
        self.headers = {
            'Host': 'my.163.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'TE': 'Trailers'
        }
        self.cache_kwargs = {}


    def start_requests(self):
        return [
                # scrapy.Request("https://my.163.com/news/remen/index.html",
                #                method='GET',
                #                callback=self.parse_activity,
                #                headers=self.headers),
                # scrapy.Request("https://my.163.com/news/news/",
                #            method='GET',
                #            callback=self.parse_news,
                #            headers=self.headers),
                # scrapy.Request("https://my.163.com/news/weihu/",
                #            method='GET',
                #            callback=self.parse_notice,
                #            headers=self.headers),
                scrapy.Request("https://my.163.com/news/xinfu/",
                           method='GET',
                           callback=self.parse_new_server,
                           headers=self.headers),
               ]

    #解析活动栏数据
    def parse_activity(self, response):
        activity_li = response.xpath("/html/body/div[3]/div[4]/div/div[3]/ul/li")
        for li in activity_li:
            item = NoticeSpiderItem()
            item['notice_type'] = '活动开启'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(li)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = ''  # 公告横幅图
            item['notice_content'] = self.extract_notice_content(li)# 公告正文
            item['notice_ext'] = '' # 公告补充文段
            item['notice_redirect_url'] = self.extract_notice_redirect_url(li)  # 公告跳转地址
            item['notice_icon_title'] = ''  # 公告按钮文案
            item['notice_id'] = self.extract_notice_id(li) # 公告 ID
            item['notice_pic'] = ''  # 公告插屏大图
            item['notice_label'] = ''  # 公告标签
            item['notice_timestamp'] = self.extract_notice_timestamp(li)# 公告通知时间
            item['notice_live_time'] = ''  # 公告持续时间
            item['notice_belong'] = ''  # 所属
            yield item

        if '下一页' in response.xpath('/html/body/div[3]/div[4]/div/div[3]/div/a/i').xpath('string()').extract():
            print('存在下一页,当前第{}页'.format(self.activity_page))
            self.activity_page += 1
            yield scrapy.Request("https://my.163.com/news/remen/index_{}.html".format(self.activity_page),
                               method='GET',
                               callback=self.parse_activity,
                               headers=self.headers)
        else:
            print('不存在下一页')

    #解析新闻栏数据
    def parse_news(self, response):
        activity_li = response.xpath("/html/body/div[3]/div[4]/div/div[3]/ul/li")
        for li in activity_li:
            item = NoticeSpiderItem()
            item['notice_type'] = '新闻'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(li)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = ''  # 公告横幅图
            item['notice_content'] = self.extract_notice_content(li)# 公告正文
            item['notice_ext'] = '' # 公告补充文段
            item['notice_redirect_url'] = self.extract_notice_redirect_url(li)  # 公告跳转地址
            item['notice_icon_title'] = ''  # 公告按钮文案
            item['notice_id'] = self.extract_notice_id(li) # 公告 ID
            item['notice_pic'] = ''  # 公告插屏大图
            item['notice_label'] = ''  # 公告标签
            item['notice_timestamp'] = self.extract_notice_timestamp(li)# 公告通知时间
            item['notice_live_time'] = ''  # 公告持续时间
            item['notice_belong'] = ''  # 所属
            yield item

        if '下一页' in response.xpath('/html/body/div[3]/div[4]/div/div[3]/div/a/i').xpath('string()').extract():
            print('存在下一页,当前第{}页'.format(self.news_page))
            self.news_page += 1
            yield scrapy.Request("https://my.163.com/news/news/index_{}.html".format(self.news_page),
                               method='GET',
                               callback=self.parse_news,
                               headers=self.headers)
        else:
            print('不存在下一页')

    #解析公告栏数据
    def parse_notice(self, response):
        activity_li = response.xpath("/html/body/div[3]/div[4]/div/div[3]/ul/li")
        for li in activity_li:
            item = NoticeSpiderItem()
            item['notice_type'] = '公告'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(li)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = ''  # 公告横幅图
            item['notice_content'] = self.extract_notice_content(li)# 公告正文
            item['notice_ext'] = '' # 公告补充文段
            item['notice_redirect_url'] = self.extract_notice_redirect_url(li)  # 公告跳转地址
            item['notice_icon_title'] = ''  # 公告按钮文案
            item['notice_id'] = self.extract_notice_id(li) # 公告 ID
            item['notice_pic'] = ''  # 公告插屏大图
            item['notice_label'] = ''  # 公告标签
            item['notice_timestamp'] = self.extract_notice_timestamp(li)# 公告通知时间
            item['notice_live_time'] = ''  # 公告持续时间
            item['notice_belong'] = ''  # 所属
            yield item

        if '下一页' in response.xpath('/html/body/div[3]/div[4]/div/div[3]/div/a/i').xpath('string()').extract():
            print('存在下一页,当前第{}页'.format(self.notice_page))
            self.notice_page += 1
            yield scrapy.Request("https://my.163.com/news/weihu/index_{}.html".format(self.notice_page),
                               method='GET',
                               callback=self.parse_notice,
                               headers=self.headers)
        else:
            print('不存在下一页')

    #解析新服数据
    def parse_new_server(self, response):
        activity_li = response.xpath("/html/body/div[3]/div[4]/div/div[3]/ul/li")
        for li in activity_li:
            item = NoticeSpiderItem()
            item['notice_type'] = '新服通知'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(li)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = ''  # 公告横幅图
            item['notice_content'] = self.extract_notice_content(li)# 公告正文
            item['notice_ext'] = '' # 公告补充文段
            item['notice_redirect_url'] = self.extract_notice_redirect_url(li)  # 公告跳转地址
            item['notice_icon_title'] = ''  # 公告按钮文案
            item['notice_id'] = self.extract_notice_id(li) # 公告 ID
            item['notice_pic'] = ''  # 公告插屏大图
            item['notice_label'] = ''  # 公告标签
            item['notice_timestamp'] = self.extract_notice_timestamp(li)# 公告通知时间
            item['notice_live_time'] = ''  # 公告持续时间
            item['notice_belong'] = ''  # 所属
            yield item

        if '下一页' in response.xpath('/html/body/div[3]/div[4]/div/div[3]/div/a/i').xpath('string()').extract():
            print('存在下一页,当前第{}页'.format(self.new_server_page))
            self.new_server_page += 1
            yield scrapy.Request("https://my.163.com/news/xinfu/index_{}.html".format(self.new_server_page),
                               method='GET',
                               callback=self.parse_new_server,
                               headers=self.headers)
        else:
            print('不存在下一页')



    def extract_notice_type(self, li):
        pass

    def extract_notice_content_type(self, li):
        pass

    def extract_notice_title(self, li):
        title = li.xpath('a/span[2]').xpath('string()').extract()[0].strip()
        self.cache_kwargs['title'] = title
        return title

    def extract_notice_id(self, li):
        redirect_url = self.cache_kwargs.get('url', '')
        title = self.cache_kwargs.get('title', '')
        src = redirect_url + str(title)
        m = hashlib.md5()
        m.update(src.encode())
        notice_id = m.hexdigest()
        return notice_id

    def extract_notice_banner_pic(self, li):
        pass

    def extract_notice_content(self, li):
        text = li.xpath('a/span[3]').xpath('string()').extract()[0].strip()
        return text

    def extract_notice_ext(self, li):
        pass

    def extract_notice_redirect_url(self, li):
        url = li.xpath('a/@href').extract()[0]
        self.cache_kwargs['url'] = url
        if url.startswith('//'):
             new_url = 'https:' + url
             return new_url
        return url

    def extract_notice_timestamp(self, li):
        pub_time = li.xpath('a/span[1]/@data-date').extract()[0].strip()
        return pub_time

    def extract_notice_icon(self, li):
        pass

    def extract_notice_icon_title(self, li):
        pass
    def extract_notice_pic(self, li):
        pass
    def extract_notice_label(self, li):
        pass

    def extract_notice_live_time(self, li):
        pass
    def extract_notice_belong(self, li):
        pass

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