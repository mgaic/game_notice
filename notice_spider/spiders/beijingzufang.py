# -*- coding: utf-8 -*-
import hashlib
import scrapy
from notice_spider.items import RentSpiderItem
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
        self.list_cookies = {
            'uniqueName': '95a01389f2b3fc637829ffb3836cde09',
            'XSRF-TOKEN': 'eyJpdiI6IkxlSVZaUzB6SHlVd0xjOHptd1ZXclE9PSIsInZhbHVlIjoiMUMyUDNsNnh1N2M0Y1c2VDZmXC9Ea1hCRlwvK1FHeTlWQWNKVXlHcTVPK2cyMnU1ZWx3eFI5dW04QVFkN3l4UFgwUlBVOGIxRVFVNG5LZ3FYMnFnRFRjdz09IiwibWFjIjoiZGI4YTE0NjMyNDE5OGViOWNjZGUyNDkxZjQ4MmJjNTZmMGExODg4YTJhYzk0Nzc2MGMyNzBlYjdjMzk2NWE2OCJ9',
            'www_sofang_session': 'eyJpdiI6IlZjcUNYVGdCbHR5UXBPTkhXbmd6OUE9PSIsInZhbHVlIjoicmhXRnlUZk9pM2NmWWJGZEpCdnNhMThUajNzNVNMaG1tVDVLRWNkWm53UWlmdHpwYXhDKzFoVEpMZUdlVGo4dkZ2Wm5JVjNQTkF6Q3oyZXhNUTNVUkE9PSIsIm1hYyI6IjRjOTI3NzkyNTViOWE1NzUxNWFlMjliMzg3MTA3OTVkMzNhNjVjZTRmY2YzZTg5Yzc1ODM4MjIyMTY4NWU0ZTAifQ%3D%3D',
            'cityid': 'eyJpdiI6Ilk3bGVUcGhzS1BGMlJXQnA3YUo0V3c9PSIsInZhbHVlIjoiWXQ4ZkluXC9jUzVYV00yaTQxU1VhYUE9PSIsIm1hYyI6IjdmNDg4ZGJiN2JiZDIwOTIzNDM4ZGM1MTdiNjA3MDAyN2Y0MWMxZjNiMDBiNjMzMDM4NWZlYTNlYTRiNzBkZDYifQ%3D%3D',
            'city': 'eyJpdiI6IndsdWtXd21FdkJKeEtrN3JFT0ZrZnc9PSIsInZhbHVlIjoiMlpxRjhcL0wwcXlFa1hmM0pOUlF5XC9UakFBUkIzUjJBbUtkT003eVdrWXFcL2toQ3R3elg3QmZDOWY0RjhDVDFnQjZodFhyRjBrMXo2MFA1U2NXbWFTem4wdjRtZDhscktWMXdubEF6Nyt4MWY2anVoVmRVaml6Rk82OTNnSUxxc05LbHVwUDR0S1QwbSszb3Vqb2dqeW5jejJOcHIwdGdockxSNkdMZUR5T21RYThEZ1NGRGI5aElQUWhkUzQ0dnVjVXRqOXVTREhHaFhCbDdTKzU5YUl4ODB0OHpyR21MRFMwSDRUb2hRY1FWa0NnTFdKOXA3YkNLWmdFem9UMW9QVW1GS2crRmdXbVowMzN1Q054eDNpTkFsV2lKK0VTYmkxQUJyNmVXemxuMVk9IiwibWFjIjoiMGNiNTg0Y2E5MWMxYjMyMjFmZjMyMjcxM2Q0Yjg0NTUxNDE5Nzc4MjJiNGFjMDhhMjc2YjRjNDVhYTY3MjMyZiJ9',
            'citypy': 'eyJpdiI6ImdxS1pTV0ZEREVWeHBmY1VJU0ZISGc9PSIsInZhbHVlIjoiZzlQNnRnZTNTeUVzemc5VnJ2dWhjQT09IiwibWFjIjoiODNmZDg1ZTg5YzNjOTBhODhlNGIxNmE1ZmZhMzliODI0ODY5ZmE1NjBhY2M5NWQ4NWNmM2ZlMTJiYmMxNzNjOCJ9',
            'codeNum': 'eyJpdiI6IlZDT0JNM3prSTJmeE1QckVYSE9Vc3c9PSIsInZhbHVlIjoiNlIzemJ4ekZPOVwvWTR3Q05MdlJWK3lJaWs1N0cwRXhsVXdhOFZTdkZ6TlpRbEdOeW5yc2J0YU9wSEFEQ3lNVVIiLCJtYWMiOiJkZDY4NGYyYzZmNGY4ZDljN2JiM2M2ZDk2OGY1ZGZkYzhmMjlhOWRkNzI3NGQ1OGMyZGUzZjU1MTg1YzRjYjcyIn0%3D',
        }
        self.detail_cookies = {
            'uniqueName': '3b06ab442df24f38f39548fd99f57715',
            'XSRF-TOKEN': 'eyJpdiI6InoyelwveXBqY2hPWVJ3MThjbzhueWRBPT0iLCJ2YWx1ZSI6Im5pQUs5alhVNTZnMEY5RVNUQWdBQUY0eERcL29vNlVZMnFvWTgrMkFFUCtQZmJvb0N2KytCSE8ydVVXTHVRdEtUcUVKUmhlVTF0ekg5dVwvQ3hDRDBiQ2c9PSIsIm1hYyI6IjNmOWFjN2ExNWRkZjU0ODlmMGM3OWFmMTk0YmRkMDdmMDFlOTJkZWVjOGY3ODA1OWFjNjgxOWRkYzMxNzgzYjMifQ%3D%3D',
            'www_sofang_session': 'eyJpdiI6IjQ0OER4d2pwaTBWUlwvZlJlekp3cE9BPT0iLCJ2YWx1ZSI6IlNCNm9RR2hHRUdwbzZaZ3dSaXh2VkpaM0g1UFwvXC9vcVwvZk5KZ1ZuZWtCdTl5Y0dKQzZjT0g0dUl4b2xyMm01cDVkK2ZpUTlmd0FsWWN2KzF3alhhVWN3PT0iLCJtYWMiOiIxOThjMGRjYzIyNjMyZGRkM2Q1YzgzZjAwZjUzNWFkNmMzZWE3Nzc5NmJmYWQ0ZjBjOTdmMDA0MDk5MTMyZDRlIn0%3D',
            'cityid': 'eyJpdiI6InRpYk9QeUsrcm1pSnhXT3I5T0pTVlE9PSIsInZhbHVlIjoiakxkTU91RUFUYng1V2NxY1lyUndaZz09IiwibWFjIjoiNzA5YWE3NDJkY2I4MzYwMDY0MzQ5N2U4MmYyYThlNDEyNTVhNjBiNzVjZGRhYzY3NjkzYmYzODM2MGZmOThhOCJ9',
            'city': 'eyJpdiI6Im03cTVId0RtK2FYN0NJTUpHOWZjc1E9PSIsInZhbHVlIjoiMW5QUWZ6QTJKM0ZqbnRDWTJlQWg2NllVOWpGVWtxQ29NT1AzbWd5Vkh6K2g0VWV3VkVFdjhnR2ZTcGliWmcweG5mcVdUck40SUdcL2ZLTnVYMXNaWG1uNFV6UmM3RTRsODdLSEhwN0lZbzlNTUpmcWhCdFRIdUdyOHA3dFZ1VVNNWitZelkwSDIrZzN4aTB3QlQ1OHF3QjhMcTM4TFVmNGdEazdEVjRUT1hpWEZnMG5mWHFhMTJsWkNcL2FsY21EQk1hemRkcmtLM2xtcGlJajhMR21jRHQ0cXJhMXFuZmp3QjZ3Z2FLQVBkajhGbGxBakdKRkZcL0NyVURDWnVnSDc1YlYyakZsQStpRm5NWDlLWHVNZWVjZkZNU0pKWm9uUFBGXC9ib2R5bHdlOVI4PSIsIm1hYyI6IjJiZTJmMmE5Nzk2MGMwYTk2Zjk1MzlkOTg1ZmY3NmUwOTllMzcxYTcxNmZiZjcxN2NjNTQ5Mjc3Mjk5NTgzYTkifQ%3D%3D',
            'citypy': 'eyJpdiI6IlJzQ1E1S2pVMXd6SXVlMkpCcUNZY0E9PSIsInZhbHVlIjoiUUk0Rk80Y240eE5Yb2FUd3FqbGhEZz09IiwibWFjIjoiNWE2YTEwZjhhZDRhZTYxY2M3N2I3YzM0OWIwNmY5NzY2MzM4MDQ0YWZjYzJkZTgwY2NkYmRkODJjYjE1ZTg1NSJ9',
            'codeNum': 'eyJpdiI6IlZDT0JNM3prSTJmeE1QckVYSE9Vc3c9PSIsInZhbHVlIjoiNlIzemJ4ekZPOVwvWTR3Q05MdlJWK3lJaWs1N0cwRXhsVXdhOFZTdkZ6TlpRbEdOeW5yc2J0YU9wSEFEQ3lNVVIiLCJtYWMiOiJkZDY4NGYyYzZmNGY4ZDljN2JiM2M2ZDk2OGY1ZGZkYzhmMjlhOWRkNzI3NGQ1OGMyZGUzZjU1MTg1YzRjYjcyIn0%3D',
        }

        self.cache_kwargs = {}


    def start_requests(self):

        return [
                #租房
                # scrapy.Request("https://bj.sofang.com/esfrent/area/bl1",
                #                method='GET',
                #                callback=self.rent_list_parse,
                #                headers=self.headers,
                #                cookies=self.list_cookies,
                #                ),
                scrapy.Request("https://bj.sofang.com/esfsale/area/bl1",
                               method='GET',
                               callback=self.esfsale_list_parse,
                               headers=self.headers,
                               cookies=self.list_cookies,
                               ),

               ]

    def esfsale_list_parse(self, response):
        dl_list = response.xpath("//div[@class='list list_free']//dl")
        for dl in dl_list:
            if self.is_direct_rent(dl):
                url = self.extract_detail_url(dl)
                yield scrapy.Request(url,
                               method='GET',
                               callback=self.esfsale_detail_parse,
                               headers=self.headers,
                               cookies=self.detail_cookies,
                               )
            else:
                continue
        page_nav_li = response.xpath("//div[@class='page_nav']/ul/li/a/text()").extract()
        if '下一页' in page_nav_li:
            self.page += 1
            print('第{}页'.format(self.page))
            yield scrapy.Request("https://bj.sofang.com/esfsale/area/bl{}".format(self.page),
                                   method='GET',
                                   callback=self.esfsale_list_parse,
                                   headers=self.headers,
                                   cookies=self.list_cookies,
                                   )
        else:
            print("下一页不存在")


    def rent_list_parse(self, response):
        dl_list = response.xpath("//div[@class='list list_free']//dl")
        for dl in dl_list:
            if self.is_direct_rent(dl):
                url = self.extract_detail_url(dl)
                yield scrapy.Request(url,
                               method='GET',
                               callback=self.rent_detail_parse,
                               headers=self.headers,
                               cookies=self.detail_cookies,
                               )
            else:
                continue
        page_nav_li = response.xpath("//div[@class='page_nav']/ul/li/a/text()").extract()
        if '下一页' in page_nav_li:
            self.page += 1
            print('第{}页'.format(self.page))
            yield scrapy.Request("https://bj.sofang.com/esfrent/area/bl{}".format(self.page),
                                   method='GET',
                                   callback=self.rent_list_parse,
                                   headers=self.headers,
                                   cookies=self.list_cookies,
                                   )
        else:
            print("下一页不存在")

    def is_direct_rent(self, dl):
        if dl.xpath('dt/span'):
            return True
        return False

    def extract_detail_url(self, dl):
        uncompleted_url = dl.xpath("dt/a/@href").extract()[0]
        complete_url = 'https://' + self.headers['Host'] + uncompleted_url
        return complete_url

    def rent_detail_parse(self, response):
        personal_div = response.xpath('//div[@class="personal"]')
        name = personal_div.xpath('p[1]/span[1]/text()').extract()[0].strip()
        tel_phone = personal_div.xpath('p[1]/span[2]/text()').extract()[0].strip()
        item = RentSpiderItem()
        item['house_type'] = '租房' # 房屋类型　
        item['personal_name'] = name# 个人姓名
        item['tel_phone'] = tel_phone  # 联系方式
        yield item

    def esfsale_detail_parse(self, response):
        personal_div = response.xpath('//div[@class="personal"]')
        name = personal_div.xpath('p[1]/span[1]/text()').extract()[0].strip()
        tel_phone = personal_div.xpath('p[1]/span[2]/text()').extract()[0].strip()
        item = RentSpiderItem()
        item['house_type'] = '二手房' # 房屋类型　
        item['personal_name'] = name# 个人姓名
        item['tel_phone'] = tel_phone  # 联系方式
        yield item