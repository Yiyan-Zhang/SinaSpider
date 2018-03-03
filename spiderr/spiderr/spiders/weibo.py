# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import time

import urllib2
import random

from spiderr.items import CommentItem,HotspotItem
import scrapy
import re
import requests
import json
from scrapy.http.request import Request
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Spider(scrapy.Spider):


    name = 'WeiboSpider'
    #allowed_domains = ['https://m.weibo.cn/p/index?containerid=106003type%253D25%2526t%253D3%2526disable_hot%253D1%2526filter_type%253Drealtimehot']
    start_urls = ['https://m.weibo.cn/p/index?containerid=106003type%253D25%2526t%253D3%2526disable_hot%253D1%2526filter_type%253Drealtimehot&title=%25E5%25BE%25AE%25E5%258D%259A%25E7%2583%25AD%25E6%2590%259C%25E6%25A6%259C&hidemenu=1&extparam=filter_type%3Drealtimehot%26mi_cid%3D%26pos%3D9%26c_type%3D30%26source%3Dranklist%26flag%3D0%26display_time%3D1508332153&luicode=10000011&lfid=106003type%3D1&featurecode=20000320%22']

    def parse(self, response):
        global driver
        limit = 0
        hotspotitem = HotspotItem()
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
        )
        driver = webdriver.PhantomJS(desired_capabilities = dcap)
        driver.get(response.url)
        titles = driver.find_elements_by_class_name('m-text-cut')

        print titles #检查网络链接


        #静态二级url
        url_2=[]
        title0 = []
        for title in titles:
            if (limit <= 50):
                title0.append(title.text)

                url2 = 'http://s.weibo.com/weibo/' + title.text.decode('unicode_escape') + '&Refer=STopic_box'
                url_2.append(url2)

                print limit, url_2
                limit = limit + 1

                print title.text.decode('unicode_escape')
                time.sleep(0.5)


            else:
                break


        for url2, newtitle in zip(url_2, title0):

            hotspotitem["title"] = newtitle


            print url2

            driver.get(url2)
            page = driver.page_source

            pattern = re.compile("mid=\w{9}")
            print pattern #检验屏蔽
            mid = re.search(pattern, page).group(0)
            mid = mid[4:]
            hotspotitem["mid1"] = mid #抓mid

            url_3 = 'https://m.weibo.cn/status/' + mid #创建三级url
            driver.get(url_3)

            author_name = driver.find_element_by_class_name('m-text-cut')
            hotspotitem["author_name"] = author_name.text

            content = driver.find_element_by_class_name('weibo-text')
            hotspotitem["content"] = content.text

            num = driver. find_elements_by_css_selector('.m-diy-btn.m-box-col.m-box-center.m-box-center-a')
            hotspotitem["replies"] = num[0].text
            hotspotitem["comments"] = num[1].text
            hotspotitem["likes"] = num[2].text

            yield hotspotitem  #抓作者名、内容、转发数、评论数、点赞数


            commentitem = CommentItem()  # 抓评论
            commentitem["mid2"] = hotspotitem["mid1"]

            pageurl = 'https://m.weibo.cn/api/comments/show?id='
            page_num = 1
            id = mid
            url_data = {
                'page': page_num,
                'id': id
            }

            while page_num:

                s = requests.get(pageurl, params=url_data)  # Request 200
                print s,page_num

                if (type(s) != dict):
                    s = s.content  # one page resource
                    # print s
                    s = json.loads(s)  # json dict

                    if s.has_key('data'):  # data非空
                    # print s
                        s = s['data']
                    # print s
                    else:
                        break


                    if s.has_key('hot_data'):
                        hot_data = s['hot_data']
                        data = s['data']
                        for item1, item2 in zip(hot_data, data):
                            commentitem["comment"] = item1['text']
                            commentitem["comment_likes"] = item1['like_counts']
                            yield commentitem
                            commentitem["comment"] = item2['text']
                            commentitem["comment_likes"] = item2['like_counts']
                            yield commentitem
                            #print item1['text'], item2['text']
                            time.sleep(0.1)
                    else:
                        data = s['data']
                        for item in data:
                            commentitem["comment"] = item['text']
                            commentitem["comment_likes"] = item['like_counts']
                            yield commentitem
                            #print item['text']
                            time.sleep(0.1)



                url_data['page'] = page_num + 1
                page_num = page_num + 1
                print page_num

            # comment = driver.find_elements_by_class_name('comment-con')
            # commentlikes = driver.find_elements_by_class_name('comment-dz-num')

            # for x, y in zip(comment, commentlikes):
            #     commentitem["comment"] = x.text
            #     commentitem["comment_likes"] = y.text
            #
            #     time.sleep(1.0)
            #
            #     yield commentitem

            time.sleep(3.0)





