# -*- coding: utf-8 -*-
import json
import scrapy
import redis
import random

class ProxySpider(scrapy.Spider):
    name = 'ProxySpider'

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def start_requests(self):
        url = 'http://icanhazip.com/'
        yield scrapy.Request(url, method='GET', callback=self.parse)

    def parse(self, response):
        print(response.text)
        return



