# -*- coding: utf-8 -*-
import hashlib
import scrapy
from notice_spider.items import NoticeSpiderItem
import redis

#大话西游爬虫
class DahuaxiyouSpider(scrapy.Spider):
    name = 'DahuaxiyouSpider'

    def __init__(self, *args, **wkargs):
        super().__init__(**wkargs)
        self.conn = redis.Redis(host='192.168.1.21', port=6379, db=8)
        self.headers = {
            'Host': 'dhxy.163.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.cache_kwargs = {}


    def start_requests(self):
        return [

                # 官方新闻入口　官方新闻内容　> 维护公告　+ 活动新闻 + 专题入口
                scrapy.Request("https://dhxy.163.com/news/",
                           method='GET',
                           callback=self.parse_news,
                           headers=self.headers),
                #活动新闻入口
                # scrapy.Request("https://dhxy.163.com/news/activity.html",
                #                method='GET',
                #                callback=self.parse_activity,
                #                headers=self.headers),

                #专题入口
                # scrapy.Request("https://dhxy.163.com/news/rmzt.html",
                #            method='GET',
                #            callback=self.parse_special_topic,
                #            headers=self.headers),
               ]

    def parse_activity(self, response):
        all_activity_a = response.xpath("(//a[@class='item'])")
        for a in all_activity_a:
            item = NoticeSpiderItem()
            item['notice_type'] = '活动新闻'  # 公告类型
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

        cur_page = int(response.xpath("(//div[@class='pagec']//em)[1]").xpath('string()').extract()[0])
        total_page = int(response.xpath("(//div[@class='pagec']//em)[2]").xpath('string()').extract()[0])
        print("第{}/{}页".format(cur_page, total_page))
        if cur_page < total_page:
            yield scrapy.Request("https://dhxy.163.com/news/activity_{}.html".format(cur_page + 1),
                                 method='GET',
                                 callback=self.parse_activity,
                                 headers=self.headers)

        else:
            print('不存在下一页')

    def parse_news(self, response):
        all_activity_a = response.xpath("(//a[@class='item'])")
        for a in all_activity_a:
            item = NoticeSpiderItem()
            item['notice_type'] = '官方新闻'  # 公告类型
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

        cur_page = int(response.xpath("(//div[@class='pagec']//em)[1]").xpath('string()').extract()[0])
        total_page = int(response.xpath("(//div[@class='pagec']//em)[2]").xpath('string()').extract()[0])
        print("第{}/{}页".format(cur_page, total_page))
        if cur_page < total_page:
            yield scrapy.Request("https://dhxy.163.com/news/index_{}.html".format(cur_page + 1),
                                 method='GET',
                                 callback=self.parse_news,
                                 headers=self.headers)

        else:
            print('不存在下一页')


    def parse_special_topic(self, response):
        all_activity_a = response.xpath("(//a[@class='item'])")
        for a in all_activity_a:
            item = NoticeSpiderItem()
            item['notice_type'] = '专题中心'  # 公告类型
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

        cur_page = int(response.xpath("(//div[@class='pagec']//em)[1]").xpath('string()').extract()[0])
        total_page = int(response.xpath("(//div[@class='pagec']//em)[2]").xpath('string()').extract()[0])
        print("第{}/{}页".format(cur_page, total_page))
        if cur_page < total_page:
            yield scrapy.Request("https://dhxy.163.com/news/rmzt_{}.html".format(cur_page + 1),
                                   method='GET',
                                   callback=self.parse_special_topic,
                                   headers=self.headers)

        else:
            print('不存在下一页')



    def extract_notice_type(self, li):
        pass

    def extract_notice_content_type(self, li):
        pass

    def extract_notice_title(self, a):
        title = a.xpath('p[1]/span[1]').xpath('string()').extract()[0].strip()
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
        content = a.xpath('p[1]/span[2]').xpath('string(.)').extract()[0].strip()
        print(content)
        return content

    def extract_notice_ext(self, a):
        pass

    def extract_notice_redirect_url(self, a):
        url = a.xpath('@href').extract()[0]
        if url.startswith('http'):
            self.cache_kwargs['url'] = url
            return url
        complete_url = 'http://' + self.headers.get('Host', '') + url
        self.cache_kwargs['url'] = complete_url
        return complete_url

    def extract_notice_timestamp(self, li):
        pub_time = li.xpath('p[2]/@data-time').extract()[0].strip()
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

