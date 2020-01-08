# -*- coding: utf-8 -*-
import hashlib
import json
import random
import scrapy
from notice_spider.items import NoticeSpiderItem
import redis

#问道爬虫
class WendaoSpider(scrapy.Spider):
    name = 'WendaoSpider'

    def __init__(self, *args, **wkargs):
        super().__init__(**wkargs)
        # self.page = 1
        self.conn = redis.Redis(host='192.168.1.21', port=6379, db=8)
        self.headers = {
            'Host': 'stzb.163.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.cache_kwargs = {}


    def start_requests(self):
        #综合栏 = 公告 + 活动 +　新闻
        return [
                #活动入口
                # scrapy.Request("http://wd.leiting.com/home/news/news_list.php?page=1&type=3",
                #                method='GET',
                #                callback=self.parse_activity,
                #                headers=self.headers),
                #新闻入口
                # scrapy.Request("http://stzb.163.com/news/",
                #                method='GET',
                #                callback=self.parse_news,
                #                headers=self.headers),
                #公告入口
                scrapy.Request("http://stzb.163.com/notice/",
                           method='GET',
                           callback=self.parse_notice,
                           headers=self.headers),
               ]

    def parse_news(self, response):
        all_activity_a = response.xpath("(//li[@class='item']//div/a)")
        for a in all_activity_a:
            item = NoticeSpiderItem()
            item['notice_type'] = '新闻'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(a)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = ''  # 公告横幅图
            item['notice_content'] = self.extract_notice_content(a)# 公告正文
            item['notice_ext'] = '' # 公告补充文段
            item['notice_redirect_url'] = self.extract_notice_redirect_url(a)  # 公告跳转地址
            item['notice_icon_title'] = ''  # 公告按钮文案
            item['notice_id'] = self.extract_notice_id(a) # 公告 ID
            item['notice_pic'] = ''  # 公告插屏大图
            item['notice_label'] = ''  # 公告标签
            item['notice_timestamp'] = self.extract_notice_timestamp(a)# 公告通知时间
            item['notice_live_time'] = ''  # 公告持续时间
            item['notice_belong'] = ''  # 所属
            yield item

        cur_page = int(response.xpath('//em[@class="cur_num"]').xpath('string()').extract()[0])
        total_page = int(response.xpath('//b[@id="total"]').xpath('string()').extract()[0])
        if cur_page < total_page:
            print('第{}/{}页'.format(cur_page,total_page))
            yield scrapy.Request("http://stzb.163.com/news/index_{}.html".format(cur_page + 1),
                               method='GET',
                               callback=self.parse_news,
                               headers=self.headers)
        else:
            print('不存在下一页')

    def parse_notice(self, response):
        all_activity_a = response.xpath("(//li[@class='item']//div/a)")
        for a in all_activity_a:
            item = NoticeSpiderItem()
            item['notice_type'] = '公告'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(a)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = ''  # 公告横幅图
            item['notice_content'] = self.extract_notice_content(a)  # 公告正文
            item['notice_ext'] = ''  # 公告补充文段
            item['notice_redirect_url'] = self.extract_notice_redirect_url(a)  # 公告跳转地址
            item['notice_icon_title'] = ''  # 公告按钮文案
            item['notice_id'] = self.extract_notice_id(a)  # 公告 ID
            item['notice_pic'] = ''  # 公告插屏大图
            item['notice_label'] = ''  # 公告标签
            item['notice_timestamp'] = self.extract_notice_timestamp(a)  # 公告通知时间
            item['notice_live_time'] = ''  # 公告持续时间
            item['notice_belong'] = ''  # 所属
            yield item

        cur_page = int(response.xpath('//em[@class="cur_num"]').xpath('string()').extract()[0])
        total_page = int(response.xpath('//b[@id="total"]').xpath('string()').extract()[0])
        if cur_page < total_page:
            print('第{}/{}页'.format(cur_page, total_page))
            yield scrapy.Request("http://stzb.163.com/notice/index_{}.html".format(cur_page + 1),
                                 method='GET',
                                 callback=self.parse_notice,
                                 headers=self.headers)
        else:
            print('不存在下一页')

    def extract_notice_type(self, li):
        pass

    def extract_notice_content_type(self, li):
        pass

    def extract_notice_title(self, a):
        title = a.xpath('p[1]/text()').extract()[0].strip()
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

    def extract_notice_banner_pic(self, a):
        pass

    def extract_notice_content(self, a):
        content = a.xpath('p[2]').xpath('string()').extract()[0].strip()
        return content

    def extract_notice_ext(self, a):
        pass

    def extract_notice_redirect_url(self, a):
        url = a.xpath('@href').extract()[0]
        if url.startswith('http'):
            self.cache_kwargs['url'] = url
            return url
        complete_url = 'http:' + url
        self.cache_kwargs['url'] = complete_url
        return complete_url

    def extract_notice_timestamp(self, li):
        try:
            return self.cache_kwargs['title'][:5]
        except:
            return ''

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

