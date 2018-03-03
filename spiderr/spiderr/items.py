# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


#class SpiderrItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
 #   pass

class CommentItem(Item):
    comment_likes = Field()  # 点赞数
    comment = Field()  # 评论
    comment_id = Field()  # 评论ID
    mid2 = Field()  # 热点ID

class HotspotItem(Item):
    """ 热点信息 """
    title = Field()  # 热点标题
    hotspot_id = Field()  # 热点ID
    content = Field()  # 热点内容
    author_name = Field()  # 作者昵称
    comments = Field()  # 评论数
    replies = Field()  # 转发数
    likes = Field()  # 点赞数
    mid1 = Field()  # 热点ID
