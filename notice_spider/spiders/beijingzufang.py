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
            'Accept-Enco３ding': 'gzip, deflate',
            'Connection': 'keep-alive',
            # 'Upgrade-Insecure-Requests': '1',
        }
        self.cookies = {
            'uniqueName': '95a01389f2b3fc637829ffb3836cde09',
            'XSRF-TOKEN': 'eyJpdiI6IkxlSVZaUzB6SHlVd0xjOHptd1ZXclE9PSIsInZhbHVlIjoiMUMyUDNsNnh1N2M0Y1c2VDZmXC9Ea1hCRlwvK1FHeTlWQWNKVXlHcTVPK2cyMnU1ZWx3eFI5dW04QVFkN3l4UFgwUlBVOGIxRVFVNG5LZ3FYMnFnRFRjdz09IiwibWFjIjoiZGI4YTE0NjMyNDE5OGViOWNjZGUyNDkxZjQ4MmJjNTZmMGExODg4YTJhYzk0Nzc2MGMyNzBlYjdjMzk2NWE2OCJ9',
            'www_sofang_session': 'eyJpdiI6IlZjcUNYVGdCbHR5UXBPTkhXbmd6OUE9PSIsInZhbHVlIjoicmhXRnlUZk9pM2NmWWJGZEpCdnNhMThUajNzNVNMaG1tVDVLRWNkWm53UWlmdHpwYXhDKzFoVEpMZUdlVGo4dkZ2Wm5JVjNQTkF6Q3oyZXhNUTNVUkE9PSIsIm1hYyI6IjRjOTI3NzkyNTViOWE1NzUxNWFlMjliMzg3MTA3OTVkMzNhNjVjZTRmY2YzZTg5Yzc1ODM4MjIyMTY4NWU0ZTAifQ%3D%3D',
            'cityid': 'eyJpdiI6Ilk3bGVUcGhzS1BGMlJXQnA3YUo0V3c9PSIsInZhbHVlIjoiWXQ4ZkluXC9jUzVYV00yaTQxU1VhYUE9PSIsIm1hYyI6IjdmNDg4ZGJiN2JiZDIwOTIzNDM4ZGM1MTdiNjA3MDAyN2Y0MWMxZjNiMDBiNjMzMDM4NWZlYTNlYTRiNzBkZDYifQ%3D%3D',
            'city': 'eyJpdiI6IndsdWtXd21FdkJKeEtrN3JFT0ZrZnc9PSIsInZhbHVlIjoiMlpxRjhcL0wwcXlFa1hmM0pOUlF5XC9UakFBUkIzUjJBbUtkT003eVdrWXFcL2toQ3R3elg3QmZDOWY0RjhDVDFnQjZodFhyRjBrMXo2MFA1U2NXbWFTem4wdjRtZDhscktWMXdubEF6Nyt4MWY2anVoVmRVaml6Rk82OTNnSUxxc05LbHVwUDR0S1QwbSszb3Vqb2dqeW5jejJOcHIwdGdockxSNkdMZUR5T21RYThEZ1NGRGI5aElQUWhkUzQ0dnVjVXRqOXVTREhHaFhCbDdTKzU5YUl4ODB0OHpyR21MRFMwSDRUb2hRY1FWa0NnTFdKOXA3YkNLWmdFem9UMW9QVW1GS2crRmdXbVowMzN1Q054eDNpTkFsV2lKK0VTYmkxQUJyNmVXemxuMVk9IiwibWFjIjoiMGNiNTg0Y2E5MWMxYjMyMjFmZjMyMjcxM2Q0Yjg0NTUxNDE5Nzc4MjJiNGFjMDhhMjc2YjRjNDVhYTY3MjMyZiJ9',
            'citypy': 'eyJpdiI6ImdxS1pTV0ZEREVWeHBmY1VJU0ZISGc9PSIsInZhbHVlIjoiZzlQNnRnZTNTeUVzemc5VnJ2dWhjQT09IiwibWFjIjoiODNmZDg1ZTg5YzNjOTBhODhlNGIxNmE1ZmZhMzliODI0ODY5ZmE1NjBhY2M5NWQ4NWNmM2ZlMTJiYmMxNzNjOCJ9',
            'codeNum': 'eyJpdiI6IlZDT0JNM3prSTJmeE1QckVYSE9Vc3c9PSIsInZhbHVlIjoiNlIzemJ4ekZPOVwvWTR3Q05MdlJWK3lJaWs1N0cwRXhsVXdhOFZTdkZ6TlpRbEdOeW5yc2J0YU9wSEFEQ3lNVVIiLCJtYWMiOiJkZDY4NGYyYzZmNGY4ZDljN2JiM2M2ZDk2OGY1ZGZkYzhmMjlhOWRkNzI3NGQ1OGMyZGUzZjU1MTg1YzRjYjcyIn0%3D',
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
                               cookies=self.cookies,
                               # dont_filter=True,
                               ),
                #合租房源
                # scrapy.Request("https://bj.sofang.com/esfrent/area/ar2",
                #            method='GET',
                #            callback=self.cooperate_rent_parse,
                #            headers=self.headers),
               ]

    def tatol_rent_parse(self, response):
        # print("123"+response.text)
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

    def parse_num(self, response):
        response.xpath("(//div[@class='info_r']//div)[3]")




