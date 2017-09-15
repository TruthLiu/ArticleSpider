# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import datetime
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



#=================以下是对item_loader获取的数组进行解析==================================
#这个value实际上就是item数组中的值
def add_jobbole(value):
    return value+"---second"

def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date

def get_nums(value):
    match_re=re.match(".*?(\d+).*",value)
    if match_re:
        nums=match_re.group(1)
    else:
        nums=0
    return nums

def remove_comment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value

#原本就是数组，所以我们不需要修改
def return_value(value):
    return value


#让articleitemloader重载itemloader 不用我们每次都调用takefirst函数
class ArticleItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()

class JobBoleArticleItem(scrapy.Item):
    #通过这种方法可以给字段加信息 如：'100:10:1方法 : 我是这样参与开源的jobbole'
    title=scrapy.Field(
        #mapcompose最多只能传入两个值，
        input_processor=MapCompose(lambda x:x+"---first",add_jobbole)
    )
    create_date=scrapy.Field(
        input_processor=MapCompose(date_convert)
        #获取数组中的第一个
        #output_processor=TakeFirst()
    )
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    front_image_url=scrapy.Field(
        #这里传入的url必须为数组，否则会报错，但是我们经过default_output_processor之后变成了str
        #这里我们就要复写output
        output_processor=MapCompose(return_value)
    )
    front_image_path=scrapy.Field()
    thumbup_nums=scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    bookmark_nums=scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums=scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    content=scrapy.Field()
    tags=scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        #我们获取的本来就是list数组，我们要将他们合并起来 Join函数即可
        output_processor=Join(",")
    )




class LagouItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()

class LagouJob(scrapy.Item):
    #拉勾网职位信息
    title=scrapy.Field()
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    salary=scrapy.Field()
    job_city=scrapy.Field()
    work_years=scrapy.Field()
    degree_need=scrapy.Field()
    job_type=scrapy.Field()
    publish_time=scrapy.Field()
    job_advantage=scrapy.Field()
    job_desc=scrapy.Field()
    job_addr=scrapy.Field()
    company_name=scrapy.Field()
    company_url=scrapy.Field()
    tags=scrapy.Field()
    crawl_time=scrapy.Field()