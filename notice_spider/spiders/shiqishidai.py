# -*- coding: utf-8 -*-
import hashlib
import json
import random
import scrapy
from notice_spider.items import NoticeSpiderItem
import redis

#官网翻页有错误,暂时不做抓取
class ShiqishidaiSpider(scrapy.Spider):
    name = 'ShiqishidaiSpider'

    def __init__(self, *args, **wkargs):
        super().__init__(**wkargs)
        self.conn = redis.Redis(host='192.168.1.21', port=6379, db=8)
        self.headers = {
            'Host': 'www.stoneage.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'http://www.stoneage.cn/index.php/list?cid=2&index=1'
            # 'Cookie': 'PHPSESSID=k9dop4istk1iuc1duvr65tu11a; Hm_lvt_7b7d42a96917963c088ca54f832463c9=1578037301; Hm_lpvt_7b7d42a96917963c088ca54f832463c9=1578038723'
        }
        self.cache_kwargs = {}


    def start_requests(self):
        return [

                scrapy.Request("http://www.stoneage.cn/article/ajax-list?cid=2&index=1&page=1&page_size=8&_=1578038723587",
                               method='GET',
                               callback=self.parse,
                               headers=self.headers),
               ]

    def parse(self, response):
        print(response.text)
        with open('shiqishidai.txt', 'w') as f:
            f.write(response.text)
        # activity_li = response.xpath("/html/body/div[3]/div[4]/div/div[2]/div[3]")
        # print(activity_li.extract())
        exit()
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

        next_page = response.xpath('//a[@title="下一页"]')
        if next_page:
            next_page_url = 'http://' + self.headers.get('Host', '') + next_page.xpath('@href').extract()[0]
            print('存在下一页')
            yield scrapy.Request(next_page_url,
                               method='GET',
                               callback=self.parse,
                               headers=self.headers)
        else:
            print('不存在下一页')



    def extract_notice_type(self, li):
        pass

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
        if url.startswith('http'):
            self.cache_kwargs['url'] = url
            return url
        complete_url = 'http://' + self.headers.get('Host', '') + url
        self.cache_kwargs['url'] = complete_url
        return complete_url

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

