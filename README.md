## 游戏公告爬虫

### 爬虫说明

- 爬取游戏公告、游戏活动、游戏运营、游戏新闻等数据
- 基于scrapy,包含一系列中间件
- spiders目录下有相应的爬虫文件以及对应的数据解析文件.json文件
- 

### 数据定义
- 公告类型: 例活动预告，升级通知，运营通知，活动预告等
- 游戏公告内容类型：例图文，HTML
- 公告标题
- 公告图标
- 公告横幅图
- 公告正文
- 公告补充文段
- 公告跳转地址
- 公告按钮文案
- 公告插屏大图
- 公告标签
- 公告通知时间
- 公告持续时间

### 爬取进度(已完成)
- 梦幻西游手游官网　新服、活动、公告、新闻等内容(https://my.163.com/news/remen/index.html)
- 诛仙手游官网     新闻、公告、活动内容(http://zx.wanmei.com/news/gameevent/index.html)
- 寻仙手游官网     新闻、公告、活动内容(http://xxsy.qq.com/webplat/info/news_version3/27244/27245/27260/27263/m18249/list_1.shtml)
- 问道手游官网     新闻、公告、活动内容(http://wd.leiting.com/home/news/news_list.php?page=1&type=2)
- 天龙八部手游官网  最新、新闻、公告、活动内容(https://tlsy.cy.com/list/hd/)
- 起源女神手游官网 攻略、公告、新闻、活动内容(http://qyns.zlongame.com/jx/qynsyxgl/)
- 斗罗大陆手游官网　新闻中心内容(包含活动、新闻、公告等 http://dl.qidian.com/index.php/home/dldl/newsList) 
- 王者荣耀手游官网 包含新闻中心、公告、活动等内容(https://pvp.qq.com/web201706/newsindex.shtml)
- 和平精英手游官网　包含公告、活动、信息等内容(https://gp.qq.com/web201908/list_news.html)
- 阴阳师完全活动单个页面解析　下一步解析整个活动栏内容 (https://yys.163.com/news/huodong/index.html)
- 阴阳师全活动、公告、新闻栏解析完成
- 三国志战略版 活动、公告、新闻栏数据 (https://sgz.ejoy.com/act/)
- 新笑傲江湖　活动、公告、新闻栏 (http://xxa.wanmei.com/news/gameevent/list.html)
- 少年三国志　活动、公告、新闻栏　(http://sg2.youzu.com/m/news.html)(ajax回传内容格式为html文本)
- 权利的游戏　活动、公告、新闻栏目(https://quanyou.qq.com/gicp/news/616/2/11918/1.html)
- 明日方舟   活动、公告、新闻栏数据采集　(https://ak.hypergryph.com/news.html)
- 梦幻西游三维版　媒体、新服、活动、公告、新闻等栏目数据(https://xy3d.163.com/news/update/)
- 率土之滨 公告栏、新闻栏　(http://stzb.163.com/news/)
- 大话西游　已完成专题中心　(https://dhxy.163.com/news/rmzt.html)
- 大话西游　专题中心、活动新闻、官方新闻　(https://dhxy.163.com/news/)
- 火影忍者爬虫　新闻、活动、公告等数据 (https://hyrz.qq.com/webplat/info/news_version3/11946/23790/23792/23935/23936/m15040/list_1.shtml)
- 乱世王者爬虫　资讯、活动、攻略等信息(https://slg.qq.com/newlist.html?iTag=12833&page=1)
- 红警OL爬虫　　新闻、公告、活动栏信息 (http://hongjing.qq.com/web201809/newslist.html?iType=7013&page=1)
- 魂斗罗归来爬虫　新闻、活动、公告栏信息(https://hdl.qq.com/webplat/info/news_version3/21518/27453/27454/27457/m17725/list_1.shtml)
- 跑跑卡丁车　活动、新闻、公告栏数据(https://wepop.qq.com/list.shtml)


### 爬取过程


- 踩坑，服务端返回的数据还是要好好看.
- 和平精英以及红警OL应该是一个团队写的,回传数据皆在js文件中,费了一点时间,最后通过charles抓包全局搜索关键字找到数据对应的位置
### End 