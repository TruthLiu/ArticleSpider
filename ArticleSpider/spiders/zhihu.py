# -*- coding: utf-8 -*-
import json
import re

#上个为python2的下面为python3
try:
    import urlparse as parse
except:
    from urllib import parse

import scrapy


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    # 设置代理
    agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
    header = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com/",
        "User-Agent": agent
    }


    def parse(self, response):
        #提取出html页面中的所有url，并跟踪这些url进行进一步爬取
        #如果提取的url中格式 /question/xxx 就下载之后直接进入解析函数
        all_urls=response.css("a::attr(href)").extract()
        all_urls=[parse.urljoin(response.url,url) for url in all_urls]
        all_url1=filter(lambda x:True if x.startswith("https") else False,all_urls)
        for url in all_url1:
           pass

    def parse_detail(self,response):
        pass


    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/#signin',headers=self.header,callback=self.login)]

    def login(self,response):
        response_text=response.text
        match_re = re.search(r'.*name="_xsrf" value="(.*?)"', response_text,re.DOTALL)
        xsrf=''
        if match_re:
           xsrf=match_re.group(1)

        if xsrf:
            return [scrapy.FormRequest(
                url="https://www.zhihu.com/login/phone_num",
                formdata={
                    "_xsrf": xsrf,
                    "phone_num": "15137337097",
                    "password": "9638527410."
                },
                headers=self.header,
                callback=self.check_login
            )]


    def check_login(self,response):
        #验证服务器的返回数据判断是否成功
        text_json=json.loads(response.text)
        #因为验证码问题不能用if来判断
        # if "msg" in text_json and text_json["msg"]=="登录成功":
        for url in self.start_urls:
            yield scrapy.Request(url,dont_filter=True,headers=self.header)

