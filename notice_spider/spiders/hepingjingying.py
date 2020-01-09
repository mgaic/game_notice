
# -*- coding: utf-8 -*-
import hashlib
import json
import scrapy
from notice_spider.items import NoticeSpiderItem
import redis

#和平精英爬虫
class HepingjingyingSpider(scrapy.Spider):
    name = 'HepingjingyingSpider'

    def __init__(self, *args, **wkargs):
        super().__init__(**wkargs)
        self.page = 1
        self.conn = redis.Redis(host='192.168.1.21', port=6379, db=8)
        self.headers = {
            'Host': 'apps.game.qq.com',
            # 'Origin':'https://pvp.qq.com',
            'TE': 'Trailers',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer':'https://gp.qq.com/web201908/list_news.html'
        }
        self.cache_kwargs = {}


    def start_requests(self):
        #新闻　公告　活动
        #数据在js脚本中 红警与和平精英数据格式一致
        return [
                # 活动入口
                # scrapy.Request("https://apps.game.qq.com/wmp/v3.1/?p0=182&p1=searchNewsKeywordsList&page=1&pagesize=10&order=sIdxTime&r0=script&r1=NewsObj6859980257066431&type=iTarget&id=4003&source=web_pc",
                #                method='GET',
                #                callback=self.parse_activity,
                #                headers=self.headers),
                # 公告入口
                # scrapy.Request("https://apps.game.qq.com/wmp/v3.1/?p0=182&p1=searchNewsKeywordsList&page=1&pagesize=10&order=sIdxTime&r0=script&r1=NewsObj560371549035622&type=iTarget&id=4001&source=web_pc",
                #                method='GET',
                #                callback=self.parse_notice,
                #                headers=self.headers),
                # 新闻入口
                scrapy.Request("https://apps.game.qq.com/wmp/v3.1/?p0=182&p1=searchNewsKeywordsList&page=1&pagesize=10&order=sIdxTime&r0=script&r1=NewsObj6183387031111702&type=iTarget&id=4000&source=web_pc",
                               method='GET',
                               callback=self.parse_news,
                               headers=self.headers),
               ]

    def parse_activity(self, response):
        json_data = self.get_json_data(response.text)

        activity_list = json_data.get('msg', {}).get('result', [])
        for activity in activity_list:
            item = NoticeSpiderItem()
            item['notice_type'] = '活动开启'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(activity)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = self.extract_notice_banner_pic(activity)  # 公告横幅图
            item['notice_content'] = ''  # 公告正文
            item['notice_ext'] = ''  # 公告补充文段
            item['notice_redirect_url'] = self.extract_notice_redirect_url(activity)  # 公告跳转地址
            item['notice_icon_title'] = ''  # 公告按钮文案
            item['notice_id'] = self.extract_notice_id(activity)  # 公告 ID
            item['notice_pic'] = ''  # 公告插屏大图
            item['notice_label'] = ''  # 公告标签
            item['notice_timestamp'] = self.extract_notice_timestamp(activity)  # 公告通知时间
            item['notice_live_time'] = ''  # 公告持续时间
            item['notice_belong'] = ''  # 所属
            yield item
        total_page = json_data.get('msg', {}).get('totalpage', 1)
        if self.page < total_page:
            print('当前第{}页'.format(self.page))
            self.page += 1
            yield scrapy.Request("https://apps.game.qq.com/wmp/v3.1/?p0=182&p1=searchNewsKeywordsList&page={}&pagesize=10&order=sIdxTime&r0=script&r1=NewsObj6859980257066431&type=iTarget&id=4003&source=web_pc".format(self.page),
                                 method='GET',
                                 callback=self.parse_activity,
                                 headers=self.headers)
        else:
            print('不存在下一页')

    def parse_news(self, response):
        json_data = self.get_json_data(response.text)
        activity_list = json_data.get('msg', {}).get('result', [])
        for activity in activity_list:
            item = NoticeSpiderItem()
            item['notice_type'] = '新闻'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(activity)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = self.extract_notice_banner_pic(activity)  # 公告横幅图
            item['notice_content'] = ''  # 公告正文
            item['notice_ext'] = ''  # 公告补充文段
            item['notice_redirect_url'] = self.extract_notice_redirect_url(activity)  # 公告跳转地址
            item['notice_icon_title'] = ''  # 公告按钮文案
            item['notice_id'] = self.extract_notice_id(activity)  # 公告 ID
            item['notice_pic'] = ''  # 公告插屏大图
            item['notice_label'] = ''  # 公告标签
            item['notice_timestamp'] = self.extract_notice_timestamp(activity)  # 公告通知时间
            item['notice_live_time'] = ''  # 公告持续时间
            item['notice_belong'] = ''  # 所属
            yield item
        total_page = json_data.get('msg', {}).get('totalpage', 1)
        if self.page < total_page:
            print('当前第{}页'.format(self.page))
            self.page += 1
            yield scrapy.Request("https://apps.game.qq.com/wmp/v3.1/?p0=182&p1=searchNewsKeywordsList&page={}&pagesize=10&order=sIdxTime&r0=script&r1=NewsObj6183387031111702&type=iTarget&id=4000&source=web_pc".format(self.page),
                                method='GET',
                                callback=self.parse_news,
                                headers=self.headers)
        else:
            print('不存在下一页')

    def parse_notice(self, response):
        json_data = self.get_json_data(response.text)

        activity_list = json_data.get('msg', {}).get('result', [])
        for activity in activity_list:
            item = NoticeSpiderItem()
            item['notice_type'] = '公告'  # 公告类型
            item['notice_content_type'] = 'HTML'  # 公告内容类型
            item['notice_title'] = self.extract_notice_title(activity)  # 公告标题
            item['notice_icon'] = ''  # 公告图标
            item['notice_banner_pic'] = self.extract_notice_banner_pic(activity)  # 公告横幅图
            item['notice_content'] = ''  # 公告正文
            item['notice_ext'] = ''  # 公告补充文段
            item['notice_redirect_url'] = self.extract_notice_redirect_url(activity)  # 公告跳转地址
            item['notice_icon_title'] = ''  # 公告按钮文案
            item['notice_id'] = self.extract_notice_id(activity)  # 公告 ID
            item['notice_pic'] = ''  # 公告插屏大图
            item['notice_label'] = ''  # 公告标签
            item['notice_timestamp'] = self.extract_notice_timestamp(activity)  # 公告通知时间
            item['notice_live_time'] = ''  # 公告持续时间
            item['notice_belong'] = ''  # 所属
            yield item
        total_page = json_data.get('msg', {}).get('totalpage', 1)
        if self.page < total_page:
            print('当前第{}页'.format(self.page))
            self.page += 1
            yield scrapy.Request("https://apps.game.qq.com/wmp/v3.1/?p0=182&p1=searchNewsKeywordsList&page={}&pagesize=10&order=sIdxTime&r0=script&r1=NewsObj560371549035622&type=iTarget&id=4001&source=web_pc".format(self.page),
                                method='GET',
                                callback=self.parse_notice,
                                headers=self.headers)
        else:
            print('不存在下一页')

    def parse_tips(self, response):
        notice_li = response.xpath("(//div[@class='tempVi']//li)")
        for li in notice_li:
            item = NoticeSpiderItem()
            item['notice_type'] = '攻略'  # 公告类型
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
        if '下一页' not in response.xpath('(//a[@disabled="disabled"])').xpath('string()').extract():
            print('存在下一页,当前第{}页'.format(self.page))
            self.page += 1
            yield scrapy.Request("http://qyns.zlongame.com/jx/qynsyxgl/index_{}.html".format(self.page),
                               method='GET',
                               callback=self.parse_tips,
                               headers=self.headers)
        else:
            print('不存在下一页')



    def extract_notice_type(self, li):
        pass

    def extract_notice_content_type(self, li):
        pass

    def extract_notice_title(self, activity):
        title = activity.get('sTitle', '')
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

    def extract_notice_banner_pic(self, activity):
        uncompleted_url = activity.get('sIMG', '')
        if uncompleted_url.startswith('http'):
            return uncompleted_url
        if uncompleted_url.startswith('//') :
            complete_url = 'http:' + uncompleted_url
            return complete_url
        return ''

    def extract_notice_content(self, li):
        pass

    def extract_notice_ext(self, li):
        pass

    def extract_notice_redirect_url(self, activity):
        news_id = activity.get('iNewsId', '')

        redirect_url = 'https://gp.qq.com/web201908/detail_news.html?newsid={}'.format(news_id)
        self.cache_kwargs['url'] = redirect_url
        return redirect_url


    def extract_notice_timestamp(self, activity):
        return activity.get('sCreated', '')

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

    def get_json_data(self, res):
        json_data_index = res.index('{"data')
        # with open('t.txt', 'a') as f:
        #     f.write(str(json_data) + '\n')
        json_data = res[json_data_index:-1]
        return json.loads(json_data)


