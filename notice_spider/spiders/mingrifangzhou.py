# -*- coding: utf-8 -*-
import hashlib
import json
import random
import re
import time
import scrapy
from notice_spider.items import NoticeSpiderItem
import redis


class MingrifangzhouSpider(scrapy.Spider):
    name = 'MingrifangzhouSpider'

    def __init__(self, *args, **wkargs):
        super().__init__(**wkargs)
        self.activity_page = 1
        self.news_page = 1
        self.notice_page = 1
        self.new_server_page = 1
        self.conn = redis.Redis(host='192.168.1.21', port=6379, db=8)
        self.headers = {
            'Host': 'ak.hypergryph.com',
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
                scrapy.Request("https://ak.hypergryph.com/news.html",
                               method='GET',
                               callback=self.parse,
                               headers=self.headers),
                # scrapy.Request("https://my.163.com/news/news/",
                #            method='GET',
                #            callback=self.parse_news,
                #            headers=self.headers),
                # scrapy.Request("https://my.163.com/news/weihu/",
                #            method='GET',
                #            callback=self.parse_notice,
                #            headers=self.headers),
                # scrapy.Request("https://my.163.com/news/xinfu/",
                #            method='GET',
                #            callback=self.parse_new_server,
                #            headers=self.headers),
               ]

    #解析活动栏数据
    def parse(self, response):
        li_list = response.xpath("(//ul[@class='news-list']//li)")
        for li in li_list:
            item = NoticeSpiderItem()
            item['notice_type'] = self.extract_notice_type(li)  # 公告类型
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

    def extract_notice_type(self, li):
        notice_label = li.xpath('a/span[2]').xpath('string()').extract()[0].strip()
        if notice_label == '活动':
            return '活动开启'
        if notice_label == '新闻':
            return '新闻'
        return '公告'

    def extract_notice_content_type(self, li):
        pass

    def extract_notice_title(self, li):
        title = li.xpath('a/h1').xpath('string()').extract()[0].strip()
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
        return ''

    def extract_notice_ext(self, li):
        pass

    def extract_notice_redirect_url(self, li):
        uncompleted_url = li.xpath('a/@href').extract()[0]
        self.cache_kwargs['url'] = uncompleted_url
        completed_url = 'https://' + self.headers.get('Host', '') + uncompleted_url[1:]
        return completed_url

    def extract_notice_timestamp(self, li):
        pub_time_span = li.xpath('a/span[1]/span/text()').extract()[0].strip()
        return pub_time_span

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

