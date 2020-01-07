# -*- coding: utf-8 -*-
import hashlib
import scrapy
from notice_spider.items import NoticeSpiderItem
import redis


class BeijingzufangSpider(scrapy.Spider):
    name = 'BeijingzufangSpider'

    def __init__(self, *args, **wkargs):
        super().__init__(**wkargs)
        self.page = 1
        self.conn = redis.Redis(host='192.168.1.21', port=6379, db=8)
        self.headers = {
            'Host': 'bj.sofang.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            # 'Upgrade-Insecure-Requests': '1',
        }
        self.cache_kwargs = {}


    def start_requests(self):
        #北京租房信息
        return [
                #整租房源
                scrapy.Request("https://bj.sofang.com/esfrent/area/bl2",
                               method='GET',
                               callback=self.tatol_rent_parse,
                               headers=self.headers,
                               dont_filter=True
                               ),
                #合租房源
                # scrapy.Request("https://bj.sofang.com/esfrent/area/ar2",
                #            method='GET',
                #            callback=self.cooperate_rent_parse,
                #            headers=self.headers),
               ]

    def tatol_rent_parse(self, response):
        print("123"+response.text)
        dl_list = response.xpath("//div[@class='list list_free']//dl")
        print(len(dl_list))
        redict_rent_list = []
        for dl in dl_list:
            if self.is_direct_rent(dl):
                print("业主直租")
            else:
                continue
    def is_direct_rent(self, dl):
        # print(dl.xpath('dt/span'))
        if dl.xpath('dt/span'):
            return True
        return False



