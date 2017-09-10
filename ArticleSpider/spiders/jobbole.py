# -*- coding: utf-8 -*-
import re

import datetime
import scrapy

from scrapy.http import Request

from urllib import parse

from scrapy.loader import ItemLoader

from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader

from ArticleSpider.utils.common import get_md5

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
#=================xpath解析========================
        # 标题的位置
       # // *[ @ id = "post-112384"] / div[1] / h1
       # /html/body/div[3]/div[3]/div[1]/div[1]/h1
       #  re_selector1=response.xpath("/html/body/div[1]/div[3]/div[1]/div[1]/h1")
        # re_selector2=response.xpath('// *[ @ id = "post-112384"] / div[1] / h1/text()')
       # re_selector=response.xpath('//div[@class="entry-header"]/h1/text() ')
        # re_selector4=response.xpath('//*[@id="post-112384"]/div[2]/p/text()[1]')
        #create_time=response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].split()[0]
        #thumbup_nums=int(response.xpath("//span[@class=' btn-bluet-bigger href-style vote-post-up   register-user-only ']/h10/text()").extract()[0])
        # bookmark_nums=response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        # match_re=re.match(r"\s*?(\d*)\s*收藏",bookmark_nums)
        # print("----------------------")
        # print(match_re.group((1)))
        # print("---------------------)-"
        #我们要判断收藏数为0的情况   “    收藏”  这就是收藏为0的情况，我们要处理
        # if match_re:
        #     if match_re.group(1)=='':
        #         bookmark_nums=0
        #     else:
        #         bookmark_nums=int(match_re.group(1))
        # comment_nums=response.xpath("//a[@href='#article-comment']/span[1]/text()").extract()[0]
        # match_re1=re.match(r"\s*?(\d*)\s*评论",comment_nums)
        #同样，我们要处理评论数为0的情况    “     评论” 这是评论为0的情况
        # if match_re1:
        #     if match_re1.group(1)=='':
        #         comment_nums=0
        #     else:
        #         comment_nums=int(match_re1.group(1))
        #
        # content=response.xpath("//div[@class='entry']").extract()[0]
        #
        # tag_list=response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # #< class 'list'>: ['IT技术', ' 1 评论 ', 'Zookeeper'] 我们要将我们不要的评论tag去掉
        # tag_list=[element for element in tag_list if not element.strip().endswith("评论")]
        # tags=",".join(tag_list)
#=====================================================================

        # 1、获取文章列表页中的文章url并交付scrapy下载后并进行解析
        # 2、获取下一页的url并交给scrapy进行下载，下载完成后交给parse

        #解析列表页中的所有文章的url并交付给scrapy下载后并进行解析
        post_nodes= response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url=post_node.css("img::attr(src)").extract_first("")
            post_url=post_node.css("::attr(href)").extract_first("")
            #response.url+post_url 对url的地址进行拼接 因为我们有时候得到post_url的值不是完整的
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_image_url":image_url},callback=self.parse_detail)

        #提取下一页并交给scrapy进行下载
        next_url=response.css(".next.page-numbers ::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    #提取文章的具体字段
    def parse_detail(self,response):
    #
    #     #创建一个字典
    #     article_item=JobBoleArticleItem()
    #
    #     #使用css提取数据
    #
    #     #文章封面图
    #     front_image_url=response.meta.get("front_image_url","")
    #
    #     #获取文章的标题
    #     title=response.css(".entry-header h1::text").extract()[0]
    #     #获取文章的创建时间
    #     create_date=response.css(".entry-meta-hide-on-mobile::text").extract()[0].split()[0]
    #     #获取文章的点赞数
    #     thumbup_nums=int(response.css(".vote-post-up h10::text").extract()[0])
    #     #获取文章的收藏个数
    #     bookmark_nums=response.css(".bookmark-btn::text").extract()[0]
    #     match_re=re.match("\s*?(\d*)\s*收藏",bookmark_nums)
    #     if match_re:
    #         if match_re.group(1)=='':
    #             bookmark_nums=0
    #         else:
    #             bookmark_nums=int(match_re.group(1))
    #     #获取文章的评论个数
    #     comment_nums=response.css("a[href='#article-comment'] span::text").extract()[0]
    #     # print("=========================")
    #     # print(response.css("a[href='#article-comment'] span::text").extract())
    #     match_re1=re.match("\s*?(\d*)\s*评论",comment_nums)
    #     # print("=================")
    #     # print(match_re1.group(1))
    #     if match_re1:
    #         if match_re1.group(1)=='':
    #             comment_nums=0
    #         else:
    #             comment_nums=int(match_re1.group(1))
    #     #获取文章的标签内容s
    #     tag_list=response.css(".entry-meta-hide-on-mobile a::text").extract()
    #     tag_list=[element for element in tag_list if  not element.strip().endswith("评论")]
    #     tags=",".join(tag_list)
    #     #获取文章的内容
    #     content=response.css(".entry").extract()
    #
    #     article_item["title"]=title
    #     article_item["url"]=response.url
    #     try:
    #         create_date=datetime.datetime.strptime(create_date,"%Y/%m/%d").date()
    #     except Exception as e:
    #         create_date=datetime.datetime.now().date()
    #     article_item["create_date"]=create_date
    #     article_item["front_image_url"]=[front_image_url]
    #     article_item["thumbup_nums"]=thumbup_nums
    #     article_item["bookmark_nums"]=bookmark_nums
    #     article_item["comment_nums"]=comment_nums
    #     article_item["content"]=content
    #     article_item["tags"]=tags
    #     article_item["url_object_id"]=get_md5(response.url)



        front_image_url=response.meta.get("front_image_url","")
        #使用item_loader来解析出来我们所要的数据，作用和上边的xpath，css一样的
        item_loader=ArticleItemLoader(item=JobBoleArticleItem(),response=response)
        item_loader.add_css("title",".entry-header h1::text")
        #如果传递过来的不是统统css样式传递的，我们使用value来传值
        item_loader.add_value("url",response.url)
        item_loader.add_value("url_object_id",get_md5(response.url))
        item_loader.add_css("create_date",".entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url",[front_image_url])
        item_loader.add_css("thumbup_nums",".vote-post-up h10::text")
        item_loader.add_css("bookmark_nums",".bookmark-btn::text")
        item_loader.add_css("comment_nums","a[href='#article-comment'] span::text")
        item_loader.add_css("content",".entry")
        item_loader.add_css("tags",".entry-meta-hide-on-mobile a::text")

        article_item=item_loader.load_item()

        yield article_item

        pass
