# -*- coding: utf-8 -*-
import json

import requests
import scrapy
from ..items import TencentItem
from urllib import parse


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['careers.tencent.com']
    keyword = input("请输入职位类别:")
    keyword = parse.quote(keyword)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    }
    one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1571662975825&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'

    # start_urls = ['https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1571662975825&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex=1&pageSize=10&language=zh-cn&area=cn']

    # 重写start_requests()
    def start_requests(self):
        total = self.get_total(self.keyword)
        for i in range(1, total + 1):
            url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1571662975825&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'.format(
                self.keyword, i)
            yield scrapy.Request(
                url=url,
                callback=self.parse_html
            )

    def parse_html(self, response):
        # http://careers.tencent.com/jobdesc.html?postId=
        # https://careers.tencent.com/tencentcareer/api/post/ByPostId?postId={}&language=zh-cn
        str_res = response.text
        json_res = json.loads(str_res)
        for i in json_res['Data']['Posts']:
            postid = i['PostId']
            url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?postId={}&language=zh-cn'.format(postid)
            yield scrapy.Request(
                url=url,
                callback=self.parse_two_html,
            )

    def parse_two_html(self, response):
        item = TencentItem()
        str_res = response.text
        json_res = json.loads(str_res)
        item['title'] = json_res['Data']['RecruitPostName']
        item['duty'] = json_res['Data']['Responsibility']
        item['yaoqiu'] = json_res['Data']['Requirement']
        yield item

    def get_total(self, keyword):
        url = self.one_url.format(keyword, 1)
        html = requests.get(url=url, headers=self.headers).json()
        count = html['Data']['Count']
        if count % 10 == 0:
            total_page = count // 10
        else:
            total_page = (count // 10) + 1

        return total_page
