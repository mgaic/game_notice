# -*- coding: utf-8 -*-
import hashlib
import re

import scrapy
from notice_spider.items import NoticeSpiderItem
import redis

#梦幻西游三维版爬虫
class MenghuanxiyouSanweibanSpider(scrapy.Spider):
    name = 'MenghuanxiyouSanweibanSpider'

    def __init__(self, *args, **wkargs):
        super().__init__(**wkargs)
        self.page = 1
        self.conn = redis.Redis(host='192.168.1.21', port=6379, db=8)
        self.headers = {
            'Host': 'xy3d.163.com',
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
                # scrapy.Request("https://xy3d.163.com/news/activity/",
                #                method='GET',
                #                callback=self.parse_activity,
                #                headers=self.headers),
                #新闻入口
                # scrapy.Request("https://xy3d.163.com/news/official/",
                #                method='GET',
                #                callback=self.parse_news,
                #                headers=self.headers),
                #公告入口
                # scrapy.Request("https://xy3d.163.com/news/update/",
                #            method='GET',
                #            callback=self.parse_notice,
                #            headers=self.headers),
                #攻略入口
                # scrapy.Request("https://xy3d.163.com/strategy/",
                #            method='GET',
                #            callback=self.parse_tips,
                #            headers=self.headers),
                #新服入口
                # scrapy.Request("https://xy3d.163.com/news/xf/",
                #                method='GET',
                #                callback=self.parse_xf,
                #                headers=self.headers),
                # 媒体入口
                scrapy.Request("https://xy3d.163.com/news/medium/",
                               method='GET',
                               callback=self.parse_medium,
                               headers=self.headers),


               ]

    def parse_activity(self, response):
        all_activity_a = response.xpath("(//ul[@class='list_item']//a)")
        for a in all_activity_a:
            item = NoticeSpiderItem()
            item['notice_type'] = '活动开启'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(a)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = self.extract_notice_banner_pic(a)  # 公告横幅图
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

        if '下一页' in response.xpath('//div[@class="l-pager"]/a').xpath('string()').extract():
            print('存在下一页,当前第{}页'.format(self.page))
            self.page += 1
            yield scrapy.Request("https://xy3d.163.com/news/activity/index_{}.html".format(self.page),
                               method='GET',
                               callback=self.parse_activity,
                               headers=self.headers)
        else:
            print('不存在下一页')

    def parse_news(self, response):
        all_activity_a = response.xpath("(//ul[@class='list_item']//a)")
        for a in all_activity_a:
            item = NoticeSpiderItem()
            item['notice_type'] = '新闻'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(a)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = self.extract_notice_banner_pic(a)  # 公告横幅图
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

        if '下一页' in response.xpath('//div[@class="l-pager"]/a').xpath('string()').extract():
            print('存在下一页,当前第{}页'.format(self.page))
            self.page += 1

            yield scrapy.Request("https://xy3d.163.com/news/official/index_{}.html".format(self.page),
                                 method='GET',
                                 callback=self.parse_news,
                                 headers=self.headers)
        else:
            print('不存在下一页')

    def parse_notice(self, response):
        all_activity_a = response.xpath("(//ul[@class='list_item']//a)")
        for a in all_activity_a:
            item = NoticeSpiderItem()
            item['notice_type'] = '公告'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(a)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = self.extract_notice_banner_pic(a)  # 公告横幅图
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

        if '下一页' in response.xpath('//div[@class="l-pager"]/a').xpath('string()').extract():
            print('存在下一页,当前第{}页'.format(self.page))
            self.page += 1

            yield scrapy.Request("https://xy3d.163.com/news/update/index_{}.html".format(self.page),
                                 method='GET',
                                 callback=self.parse_notice,
                                 headers=self.headers)
        else:
            print('不存在下一页')

    def parse_tips(self, response):
        all_activity_a = response.xpath("(//ul[@class='list_item']//a)")
        for a in all_activity_a:
            item = NoticeSpiderItem()
            item['notice_type'] = '攻略'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(a)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = self.extract_notice_banner_pic(a)  # 公告横幅图
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

        if '下一页' in response.xpath('//div[@class="l-pager"]/a').xpath('string()').extract():
            print('存在下一页,当前第{}页'.format(self.page))
            self.page += 1

            yield scrapy.Request("https://xy3d.163.com/strategy/index_{}.html".format(self.page),
                                 method='GET',
                                 callback=self.parse_tips,
                                 headers=self.headers)
        else:
            print('不存在下一页')

    def parse_xf(self, response):
        all_activity_a = response.xpath("(//ul[@class='list_item']//a)")
        for a in all_activity_a:
            item = NoticeSpiderItem()
            item['notice_type'] = '新服'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(a)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = self.extract_notice_banner_pic(a)  # 公告横幅图
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

        if '下一页' in response.xpath('//div[@class="l-pager"]/a').xpath('string()').extract():
            print('存在下一页,当前第{}页'.format(self.page))
            self.page += 1

            yield scrapy.Request("https://xy3d.163.com/news/xf/index_{}.html".format(self.page),
                                 method='GET',
                                 callback=self.parse_xf,
                                 headers=self.headers)
        else:
            print('不存在下一页')

    def parse_medium(self, response):
        all_activity_a = response.xpath("(//ul[@class='list_item']//a)")
        for a in all_activity_a:
            item = NoticeSpiderItem()
            item['notice_type'] = '媒体'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(a)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = self.extract_notice_banner_pic(a)  # 公告横幅图
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

        if '下一页' in response.xpath('//div[@class="l-pager"]/a').xpath('string()').extract():
            print('存在下一页,当前第{}页'.format(self.page))
            self.page += 1

            yield scrapy.Request("https://xy3d.163.com/news/medium/index_{}.html".format(self.page),
                                 method='GET',
                                 callback=self.parse_medium,
                                 headers=self.headers)
        else:
            print('不存在下一页')


    def extract_notice_type(self, li):
        pass

    def extract_notice_content_type(self, li):
        pass

    def extract_notice_title(self, a):
        title = a.xpath('h3').xpath('string()').extract()[0].strip()
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
        style = a.xpath('div[1]/div[1]/@style').extract()[0].strip()
        try:
            return re.findall("url\(\'(.*?)\'", style)[0]
        except:
            return ''

    def extract_notice_content(self, a):
        try:
            content = a.xpath('p').xpath('string()').extract()[0].strip()
            return content
        except:
            return ''

    def extract_notice_ext(self, a):
        pass

    def extract_notice_redirect_url(self, a):
        url = a.xpath('@href').extract()[0]
        self.cache_kwargs['url'] = url
        return url

    def extract_notice_timestamp(self, li):
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

