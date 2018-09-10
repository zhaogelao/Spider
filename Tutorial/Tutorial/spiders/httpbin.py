# -*- coding: utf-8 -*-
import scrapy

#baseclass
class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/get']

    # url = 'http://httpbin.org/post'

    # def start_requests(self):
    #     yield scrapy.FormRequest(url=self.url,formdata={'kw':'python','q':'kasjdkl'},callback=self.parse)

    # def make_requests_from_url(self, url):
    #     return scrapy.Request(url,callback=self.parse_item)

    def parse(self, response):
        self.logger.info(response.status)

    # def parse_item(self,response):
    #     print('++++++++=+++++++++')
    #
    # def close(self,reason):
    #     self.logger.info(reason)
