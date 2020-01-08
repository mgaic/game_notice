# -*- coding: utf-8 -*-
import hashlib
import json
import random
import scrapy
from notice_spider.items import NoticeSpiderItem
import redis

#天龙八部爬虫
class TianlongbabuSpider(scrapy.Spider):
    name = 'TianlongbabuSpider'

    def __init__(self, *args, **wkargs):
        super().__init__(**wkargs)
        self.page = 1
        self.conn = redis.Redis(host='192.168.1.21', port=6379, db=8)
        self.headers = {
            'Host': 'tlsy.cy.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.cache_kwargs = {}


    def start_requests(self):
        #最新　新闻　公告　活动　四个栏目　最新包含新手攻略等数据分类不明确,暂时不做抓取
        return [
                #活动入口
                # scrapy.Request("https://tlsy.cy.com/list/hd/",
                #                method='GET',
                #                callback=self.parse_activity,
                #                headers=self.headers),
                # #新闻入口
                # scrapy.Request("https://tlsy.cy.com/list/xw/",
                #                method='GET',
                #                callback=self.parse_news,
                #                headers=self.headers),
                # #公告入口
                # scrapy.Request("https://tlsy.cy.com/list/gg/",
                #                method='GET',
                #                callback=self.parse_notice,
                #                headers=self.headers),
                #最新入口
                scrapy.Request("https://tlsy.cy.com/list/zx/",
                               method='GET',
                               callback=self.parse_latest,
                               headers=self.headers),
               ]

    def parse_activity(self, response):
        activity_li = response.xpath("//ul[@class='articles']/li")
        for li in activity_li:
            item = NoticeSpiderItem()
            item['notice_type'] = '活动开启'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(li)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = ''  # 公告横幅图
            item['notice_content'] = ''# 公告正文
            item['notice_ext'] = '' # 公告补充文段
            item['notice_redirect_url'] = self.extract_notice_redirect_url(li)  # 公告跳转地址
            item['notice_icon_title'] = ''  # 公告按钮文案
            item['notice_id'] = self.extract_notice_id(li) # 公告 ID
            item['notice_pic'] = ''  # 公告插屏大图
            item['notice_label'] = ''  # 公告标签
            item['notice_timestamp'] = self.extract_notice_timestamp(li)# 公告通知时间
            item['notice_live_time'] = ''  # 公告持续时间
            item['notice_belong'] = ''  # 所属
            # print(item)
            yield item
        if '下一页' in response.xpath('//div[@class="pagination"]//ul[1]/li/a').xpath('string()').extract():
            print('存在下一页,当前第{}页'.format(self.page))
            self.page += 1
            yield scrapy.Request("https://tlsy.cy.com/list/hd/index_{}.shtml".format(self.page - 1),
                               method='GET',
                               callback=self.parse_activity,
                               headers=self.headers)
        else:
            print('不存在下一页')

    def parse_news(self, response):
        activity_li = response.xpath("//ul[@class='articles']/li")
        for li in activity_li:
            item = NoticeSpiderItem()
            item['notice_type'] = '新闻'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(li)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = ''  # 公告横幅图
            item['notice_content'] = ''# 公告正文
            item['notice_ext'] = '' # 公告补充文段
            item['notice_redirect_url'] = self.extract_notice_redirect_url(li)  # 公告跳转地址
            item['notice_icon_title'] = ''  # 公告按钮文案
            item['notice_id'] = self.extract_notice_id(li) # 公告 ID
            item['notice_pic'] = ''  # 公告插屏大图
            item['notice_label'] = ''  # 公告标签
            item['notice_timestamp'] = self.extract_notice_timestamp(li)# 公告通知时间
            item['notice_live_time'] = ''  # 公告持续时间
            item['notice_belong'] = ''  # 所属
            # print(item)
            yield item
        if '下一页' in response.xpath('//div[@class="pagination"]//ul[1]/li/a').xpath('string()').extract():
            print('存在下一页,当前第{}页'.format(self.page))
            self.page += 1
            yield scrapy.Request("https://tlsy.cy.com/list/xw/index_{}.shtml".format(self.page - 1),
                               method='GET',
                               callback=self.parse_news,
                               headers=self.headers)
        else:
            print('不存在下一页')

    def parse_notice(self, response):
        activity_li = response.xpath("//ul[@class='articles']/li")
        for li in activity_li:
            item = NoticeSpiderItem()
            item['notice_type'] = '公告'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(li)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = ''  # 公告横幅图
            item['notice_content'] = ''# 公告正文
            item['notice_ext'] = '' # 公告补充文段
            item['notice_redirect_url'] = self.extract_notice_redirect_url(li)  # 公告跳转地址
            item['notice_icon_title'] = ''  # 公告按钮文案
            item['notice_id'] = self.extract_notice_id(li) # 公告 ID
            item['notice_pic'] = ''  # 公告插屏大图
            item['notice_label'] = ''  # 公告标签
            item['notice_timestamp'] = self.extract_notice_timestamp(li)# 公告通知时间
            item['notice_live_time'] = ''  # 公告持续时间
            item['notice_belong'] = ''  # 所属
            # print(item)
            yield item
        if '下一页' in response.xpath('//div[@class="pagination"]//ul[1]/li/a').xpath('string()').extract():
            print('存在下一页,当前第{}页'.format(self.page))
            self.page += 1
            yield scrapy.Request("https://tlsy.cy.com/list/gg/index_{}.shtml".format(self.page - 1),
                               method='GET',
                               callback=self.parse_notice,
                               headers=self.headers)
        else:
            print('不存在下一页')

    def parse_latest(self, response):
        activity_li = response.xpath("//ul[@class='articles']/li")
        for li in activity_li:
            item = NoticeSpiderItem()
            item['notice_type'] = self.extract_notice_type(li)  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(li)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = ''  # 公告横幅图
            item['notice_content'] = ''# 公告正文
            item['notice_ext'] = '' # 公告补充文段
            item['notice_redirect_url'] = self.extract_notice_redirect_url(li)  # 公告跳转地址
            item['notice_icon_title'] = ''  # 公告按钮文案
            item['notice_id'] = self.extract_notice_id(li) # 公告 ID
            item['notice_pic'] = ''  # 公告插屏大图
            item['notice_label'] = ''  # 公告标签
            item['notice_timestamp'] = self.extract_notice_timestamp(li)# 公告通知时间
            item['notice_live_time'] = ''  # 公告持续时间
            item['notice_belong'] = ''  # 所属
            # print(item)
            yield item
        if '下一页' in response.xpath('//div[@class="pagination"]//ul[1]/li/a').xpath('string()').extract():
            print('存在下一页,当前第{}页'.format(self.page))
            self.page += 1
            yield scrapy.Request("https://tlsy.cy.com/list/zx/index_{}.shtml".format(self.page - 1),
                               method='GET',
                               callback=self.parse_latest,
                               headers=self.headers)
        else:
            print('不存在下一页')



    def extract_notice_type(self, li):
        notice_type = li.xpath('span[1]').xpath('string()').extract()[0].strip()
        if '公告' in notice_type:
            return '公告'
        if '活动' in notice_type:
            return '活动开启'
        if '新闻' in notice_type:
            return '新闻'
        return '运营通知'

    def extract_notice_content_type(self, li):
        pass

    def extract_notice_title(self, li):
        title = li.xpath('a/text()').extract()[0].strip()
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
        pass

    def extract_notice_ext(self, li):
        pass

    def extract_notice_redirect_url(self, li):
        url = li.xpath('a/@href').extract()[0]
        # if url.startswith('http'):
        #     self.cache_kwargs['url'] = url
        #     return url
        # complete_url = 'http://' + self.headers.get('Host', '') + url
        self.cache_kwargs['url'] = url
        return url

    def extract_notice_timestamp(self, li):
        pub_time = li.xpath('span[2]').xpath('string()').extract()[0].strip()
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

