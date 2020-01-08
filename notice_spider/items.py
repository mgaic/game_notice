# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NoticeSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    notice_type = scrapy.Field()            #公告类型
    notice_content_type = scrapy.Field()         #公告内容类型
    notice_id = scrapy.Field()              #公告 ID
    notice_title = scrapy.Field()           #公告标题
    notice_icon = scrapy.Field()            #公告图标
    notice_banner_pic = scrapy.Field()   #公告横幅图
    notice_content = scrapy.Field()            #公告正文
    notice_ext = scrapy.Field()        #公告补充文段
    notice_redirect_url = scrapy.Field()      #公告跳转地址
    notice_icon_title = scrapy.Field()       #公告按钮文案
    notice_pic = scrapy.Field()#公告插屏大图
    notice_label = scrapy.Field()             #公告标签
    notice_timestamp = scrapy.Field()    #公告通知时间
    notice_live_time = scrapy.Field()       #公告持续时间
    notice_belong = scrapy.Field()     #所属服

class RentSpiderItem(scrapy.Item):
    house_type = scrapy.Field()     # 房屋类型　
    personal_name = scrapy.Field()  # 个人姓名
    tel_phone = scrapy.Field()      # 联系方式