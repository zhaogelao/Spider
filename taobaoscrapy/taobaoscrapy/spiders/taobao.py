# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
from taobaoscrapy.items import TaobaoscrapyItem


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    start_urls = ['https://s.taobao.com/search?q=']

    url_base = 'https://s.taobao.com/search?q='

    #初始请求
    def start_requests(self):
        for k in self.settings.get('KEYWORD'):
            url = self.url_base + quote(k)
            for pn in range(1,self.settings.get('MAXPAGE')+1):
                #请求，用meta来包含page信息来传输到middleware里面
                yield scrapy.Request(url=url,callback=self.parse,meta={'page':pn},dont_filter=True)

    #解析response，提取信息
    def parse(self, response):
        # print(response.text)
        results=response.xpath('//div[@class="items"]/div[contains(@class,"item")]')
        for result in results:
            item = TaobaoscrapyItem()
            #提取价格
            item['price']=result.xpath('.//div[contains(@class,"price")]/strong/text()').extract_first()
            #交易数量
            item['deal'] = result.xpath('.//div[@class="deal-cnt"]/text()').extract_first()
            #商店位置
            item['location'] = result.xpath('.//div[@class="location"]/text()').extract_first()
            #商店名
            item['shop']=''.join(result.xpath('.//div[@class="shop"]/a/span/text()').extract()).strip()
            #产品描述
            item['name']=''.join(result.xpath('.//div[contains(@class,"title")]/a//text()').extract()).strip()
            yield item