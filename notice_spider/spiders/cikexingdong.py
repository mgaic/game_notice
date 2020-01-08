# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
import json

#刺客行动爬虫
class CikexingdongSpider(scrapy.Spider):
    name = 'cikexingdongSpider'
    allowed_domains = ["https://auction.unityads.unity3d.com"]
    def __init__(self, *args, **wkargs):
        super().__init__(**wkargs)
        self.headers = {
		    'Content-Type': "application/json",
		    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 6.0; Nexus 5 Build/MRA58K)",
		    'Host': "auction.unityads.unity3d.com",
		    'Accept-Encoding': "gzip",
		    'Connection': "keep-alive",
		    'Accept': "*/*",
		    'Cache-Control': "no-cache",
		    'Postman-Token': "7e7eef8b-f207-4f6e-8d1a-a14f128dda85,05d02e71-7d61-46c0-a9cc-12f659cbf900",
		    # 'Content-Length': "2604",
		    'cache-control': "no-cache"
		}

    
        self.payload = "{\"bundleVersion\":\"1.7\",\"bundleId\":\"com.rubygames.assassin\",\"coppa\":false,\"language\":\"zh_CN\",\"gameSessionId\":89512216261516,\"timeZone\":\"GMT+08:00\",\"token\":\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWMiOjE5NiwiYXpwIjoiZWUyODM3MDUtYjQyMi00ODdhLWIxNTAtNTJjNzM2Yzg1MWMwIiwiY3BpIjoyMjgsImNyZWF0ZWQiOjE1Nzc2MjEzMDgwMDAsImV4cCI6MTU3ODkxNTU4NCwiaWFwIjoxMjcsImlhdCI6MTU3NzcwNTk4NCwiaXNzIjoiYWRzLWdhbWUtY29uZmlndXJhdGlvbi51bml0eWFkcy51bml0eTNkLmNvbSIsImx0diI6MTUyLCJwcm8iOjcxLCJzdWIiOiJkNUVWUkRZNkVEbVE4UGVrUHd2ZitybzFwNk9MRW90Q29LK0VOSCtYUDZXZ1BjNmJJSHhzdlJpekFmbERZUmtxakZlN1p3PT0iLCJ4cHIiOjEwM30.ypuzyP2vbQDHiV9rxBtmq-_RTz0KAXJrWAlKMu9AuEQ\",\"webviewUa\":\"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.117 Mobile Safari/537.36\",\"deviceFreeSpace\":25659880,\"networkOperator\":\"\",\"networkOperatorName\":\"\",\"wiredHeadset\":false,\"volume\":1,\"requestSignal\":\"CvcBChR1bml0eS1hbmRyb2lkLXYzLjIuMBAGGAK6AQM2LjDAAQTIAfipENAB7KkQ2AGAD-ABAOgBAfABAfgBAYACAYgCUpAC_sOn8AWYAtDEp_AFqgJANWQ2MjFhYWE0MWFhYWYyMTk2YWRmZTJiMTFiMTIzMjYyMTJhMjQxNDBhMzZmZmE1MTk4YmU4NzQyM2U2MDFjZbICKDM3OWRjODVjMWU0YWJhMDc4YTY0ZTE2MzU0NTk3YjNjODRiNjYzNmK6AgMxLjfAAqsBygIWY29tLnJ1YnlnYW1lcy5hc3Nhc3NpbtICB3Vua25vd26AA7gIiAPwDZADARgCIAM\",\"ext\":{\"seq_num\":1,\"granular_speed_bucket\":\"wi\",\"network_metered\":false,\"mobile_device_submodel\":\"Nexus 5\",\"prior_user_requests\":9,\"device_battery_charging\":true,\"device_battery_level\":0.06,\"android_market_version\":\"171.com.rubygames.assassin\",\"prior_click_count\":0,\"device_incapabilities\":\"mt\",\"ios_jailbroken\":true,\"iu_sizes\":\"1080x1776|1776x1080\",\"ad_load_duration\":5708},\"isPromoCatalogAvailable\":false,\"cachedCampaigns\":[\"005472656d6f7220416e6472\",\"5d037b4a0969b700268c4d83\"],\"versionCode\":171,\"mediationName\":\"MoPub\",\"mediationVersion\":\"5.9.1\",\"placements\":{\"BNR_AND_16\":{\"adTypes\":[\"BANNER\"],\"allowSkip\":true,\"dimensions\":{\"w\":320,\"h\":50}}},\"properties\":\"0Stg2usHEFjeQ3vHHFbts5ck56QSKjervViyRg/XN4klEXwYBORzoxGUJMeONrs=\",\"sessionDepth\":1,\"projectId\":\"ee283705-b422-487a-b150-52c736c851c0\",\"gameSessionCounters\":{\"adRequests\":10,\"starts\":0,\"views\":0,\"startsPerCampaign\":{},\"startsPerTarget\":{},\"viewsPerCampaign\":{},\"viewsPerTarget\":{},\"latestCampaignsStarts\":{}},\"gdprEnabled\":false,\"optOutEnabled\":false,\"optOutRecorded\":false,\"privacy\":{\"method\":\"default\",\"firstRequest\":true,\"permissions\":{\"ads\":true,\"external\":true,\"gameExp\":true}},\"abGroup\":4,\"developerId\":1600581,\"organizationId\":\"18966709832833\",\"isLoadEnabled\":false,\"omidPartnerName\":\"Unity3d\",\"omidJSVersion\":\"1.2.10\",\"legalFramework\":\"none\",\"agreedOverAgeLimit\":\"missing\"}"
    

    def start_requests(self):
        return [scrapy.Request("https://auction.unityads.unity3d.com/v5/games/3292952/requests?advertisingTrackingId=7ae88f18-d809-45d1-be56-6b672bc491f3&limitAdTracking=False&deviceModel=Nexus%25205&platform=android&sdkVersion=3200&stores=google&deviceMake=LGE&screenSize=268435794&screenDensity=480&apiLevel=23&screenWidth=1080&screenHeight=1776&connectionType=wifi&networkType=0",
                                     method='POST',
                                     callback=self.parse,
                                     headers=self.headers,
                                     body=self.payload)]

    def parse(self, response):
        print(response.text)

