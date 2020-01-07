
# -*- coding: utf-8 -*-
import hashlib
import math
import re
import scrapy
from notice_spider.items import NoticeSpiderItem
import redis
from lxml import etree
from scrapy.selector import Selector

class ShaoniansanguozhiSpider(scrapy.Spider):
    name = 'ShaoniansanguozhiSpider'

    def __init__(self, *args, **wkargs):
        super().__init__(**wkargs)
        self.page = 1
        self.conn = redis.Redis(host='192.168.1.21', port=6379, db=8)
        self.headers = {
            'Host': 'sg2.youzu.com',
            # 'Origin':'https://pvp.qq.com',
            'TE': 'Trailers',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer':'http://sg2.youzu.com/m/news.html'
        }
        self.cache_kwargs = {}


    def start_requests(self):
        #新闻　公告　活动　
        return [
                # 活动入口
                # scrapy.Request("http://sg2.youzu.com/m/active/page/1.html",
                #                method='GET',
                #                callback=self.parse_activity,
                #                headers=self.headers),
                # 公告入口
                scrapy.Request("http://sg2.youzu.com/m/notice/page/1.html",
                               method='GET',
                               callback=self.parse_notice,
                               headers=self.headers),
                # 新闻入口
                # scrapy.Request("http://sg2.youzu.com/m/news/page/1.html",
                #                method='GET',
                #                callback=self.parse_news,
                #                headers=self.headers),
               ]

    def parse_activity(self, response):
        res = Selector(text=response.text)
        news_list = res.xpath("//ul[@class='news-list']//li")
        # if len(news_list) == 0:
        #     with open("excetion_page.txt", 'w') as f:
        #         f.write(response.text)
        for news in news_list:
            item = NoticeSpiderItem()
            item['notice_type'] = '活动开启'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(news)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = self.extract_notice_banner_pic(news)  # 公告横幅图
            item['notice_content'] = self.extract_notice_content(news)  # 公告正文
            item['notice_ext'] = ''  # 公告补充文段
            item['notice_redirect_url'] = self.extract_notice_redirect_url(news)  # 公告跳转地址
            item['notice_icon_title'] = ''  # 公告按钮文案
            item['notice_id'] = self.extract_notice_id(news)  # 公告 ID
            item['notice_pic'] = ''  # 公告插屏大图
            item['notice_label'] = ''  # 公告标签
            item['notice_timestamp'] = self.extract_notice_timestamp(news)  # 公告通知时间
            item['notice_live_time'] = ''  # 公告持续时间
            item['notice_belong'] = ''  # 所属
            yield item
        total_count = int(re.findall('total = (.*?),', response.text)[0])
        total_page = math.ceil( total_count / 6 )
        if self.page < total_page:
            print('当前第{}/{}页'.format(self.page, total_page))
            self.page += 1
            yield scrapy.Request("http://sg2.youzu.com/m/active/page/{}.html".format(self.page),
                                 method='GET',
                                 callback=self.parse_activity,
                                 headers=self.headers)
        else:
            print('不存在下一页')

    def parse_news(self, response):
        res = Selector(text=response.text)
        news_list = res.xpath("//ul[@class='news-list']//li")
        if len(news_list) == 0:
            with open("excetion_page.txt", 'w') as f:
                f.write(response.text)
        for news in news_list:
            item = NoticeSpiderItem()
            item['notice_type'] = '新闻'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(news)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = self.extract_notice_banner_pic(news)  # 公告横幅图
            item['notice_content'] = self.extract_notice_content(news)  # 公告正文
            item['notice_ext'] = ''  # 公告补充文段
            item['notice_redirect_url'] = self.extract_notice_redirect_url(news)  # 公告跳转地址
            item['notice_icon_title'] = ''  # 公告按钮文案
            item['notice_id'] = self.extract_notice_id(news)  # 公告 ID
            item['notice_pic'] = ''  # 公告插屏大图
            item['notice_label'] = ''  # 公告标签
            item['notice_timestamp'] = self.extract_notice_timestamp(news)  # 公告通知时间
            item['notice_live_time'] = ''  # 公告持续时间
            item['notice_belong'] = ''  # 所属
            yield item

        total_count = int(re.findall('total = (.*?),', response.text)[0])
        total_page = math.ceil(total_count / 6) #向上取整
        if self.page < total_page:
            print('当前第{}/{}页'.format(self.page, total_page))
            self.page += 1
            yield scrapy.Request("http://sg2.youzu.com/m/news/page/{}.html".format(self.page),
                                 method='GET',
                                 callback=self.parse_news,
                                 headers=self.headers)
        else:
            print('不存在下一页')

    def parse_notice(self, response):
        res = Selector(text=response.text)
        news_list = res.xpath("//ul[@class='news-list']//li")
        # if len(news_list) == 0:
        #     with open("excetion_page.txt", 'w') as f:
        #         f.write(response.text)
        for news in news_list:
            item = NoticeSpiderItem()
            item['notice_type'] = '公告'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(news)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = self.extract_notice_banner_pic(news)  # 公告横幅图
            item['notice_content'] = self.extract_notice_content(news)  # 公告正文
            item['notice_ext'] = ''  # 公告补充文段
            item['notice_redirect_url'] = self.extract_notice_redirect_url(news)  # 公告跳转地址
            item['notice_icon_title'] = ''  # 公告按钮文案
            item['notice_id'] = self.extract_notice_id(news)  # 公告 ID
            item['notice_pic'] = ''  # 公告插屏大图
            item['notice_label'] = ''  # 公告标签
            item['notice_timestamp'] = self.extract_notice_timestamp(news)  # 公告通知时间
            item['notice_live_time'] = ''  # 公告持续时间
            item['notice_belong'] = ''  # 所属
            yield item

        total_count = int(re.findall('total = (.*?),', response.text)[0])
        total_page = math.ceil(total_count / 6)  # 向上取整
        if self.page < total_page:
            print('当前第{}/{}页'.format(self.page, total_page))
            self.page += 1
            yield scrapy.Request("http://sg2.youzu.com/m/notice/page/{}.html".format(self.page),
                                 method='GET',
                                 callback=self.parse_notice,
                                 headers=self.headers)
        else:
            print('不存在下一页')

    def extract_notice_type(self, news):
        pass

    def extract_notice_content_type(self, news):
        pass

    def extract_notice_title(self, news):
        title = news.xpath('a/p[1]').xpath('string(.)').extract()[0].strip()
        self.cache_kwargs['title'] = title
        return title

    def extract_notice_id(self, news):
        redirect_url = self.cache_kwargs.get('url', '')
        title = self.cache_kwargs.get('title', '')
        src = redirect_url + str(title)
        m = hashlib.md5()
        m.update(src.encode())
        notice_id = m.hexdigest()
        return notice_id

    def extract_notice_banner_pic(self, news):
        return ''

    def extract_notice_content(self, news):
        try:
            content = news.xpath('a/p[2]/text()').extract()[0].strip()
            return content
        except:
            return ''

    def extract_notice_ext(self, news):
        pass

    def extract_notice_redirect_url(self, news):
        url = news.xpath('a/@href').extract()[0]
        if url.startswith('http'):
            self.cache_kwargs['url'] = url
            return url
        complete_url = 'http://' + self.headers.get('Host', '') + url
        self.cache_kwargs['url'] = complete_url
        return complete_url


    def extract_notice_timestamp(self, news):
        pub_time = news.xpath('a/p[3]/text()').extract()[0].strip()
        return pub_time

    def extract_notice_icon(self, news):
        pass

    def extract_notice_icon_title(self, news):
        pass
    def extract_notice_pic(self, news):
        pass
    def extract_notice_label(self, news):
        pass

    def extract_notice_live_time(self, news):
        pass
    def extract_notice_belong(self, news):
        pass




