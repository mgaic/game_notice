# -*- coding: utf-8 -*-
import json
import time

import scrapy

from notice_spider.items import NoticeSpiderItem


class QuanmincaigeSpider(scrapy.Spider):
    name = 'QuanmincaigeSpider'
    # allowed_domains = ["http://oc.umeng.com"]

    def __init__(self, *args, **wkargs):
        super().__init__(**wkargs)
        self.headers = {
            'Host': 'oc.umeng.com',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; Nexus 5 Build/MRA58K)',
        }
    
        self.data = '{"type":"online_config","appkey":"53c2451756240b753811111b","version_code":"12","package":"cn.uqu8.guesssong","sdk_version":"1.0.0","idmd5":"f607264fc6318a92b9e13c65db7cd3c","channel":"redmi","last_config_time":0}'
    

    def start_requests(self):
        return [scrapy.Request("http://oc.umeng.com/v2/check_config_update",
                                     method='POST',
                                     callback=self.parse,
                                     headers=self.headers,
                                     body=self.data)]

    def parse(self, response):
        json_data = json.loads(response.text)
        item = NoticeSpiderItem()
        item['notice_type'] = '升级通知'  # 公告类型
        item['notice_content_type'] = '图文'  # 公告内容类型
        item['notice_id'] = json_data.get('online_params', {}).get('upgrade_mark','') # 公告 ID
        item['notice_title'] = json_data.get('online_params', {}).get('mini_notice','')  # 公告标题
        item['notice_icon'] = ''  # 公告图标
        item['notice_banner_pic'] = ''  # 公告横幅图
        item['notice_content'] = json_data.get('online_params', {}).get('upgrade_desc','')  # 公告正文
        item['notice_ext'] = json_data.get('online_params', {}).get('notice_content','')  # 公告补充文段
        item['notice_redirect_url'] = json_data.get('online_params', {}).get('tontact_url','')  # 公告跳转地址
        item['notice_icon_title'] = ''  # 公告按钮文案
        item['notice_pic'] = ''  # 公告插屏大图
        item['notice_label'] = ''  # 公告标签
        item['notice_timestamp'] = self.timestamp_to_format(json_data.get('last_config_time',''))  # 公告通知时间
        item['notice_live_time'] = '' # 公告持续时间
        item['notice_belong'] = ''  # 所属
        yield item


    def timestamp_to_format(self, timestamp=None, format='%Y-%m-%d %H:%M:%S'):
        try:
            struct_timestamp = time.localtime(timestamp // 1000)
            time_format = time.strftime("%Y-%m-%d %H:%M:%S", struct_timestamp)
            return time_format
        except:
            return ''