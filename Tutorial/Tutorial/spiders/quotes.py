# -*- coding: utf-8 -*-
import scrapy
from Tutorial.items import QuotesItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'#spider的名字
    # allowed_domains = ['www.baidu.com']#
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        print(response.encoding)
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuotesItem()
            item['text']=quote.css('.text::text').extract_first()
            item['author']=quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item

        next_page=response.css('.pager .next a::attr(href)').extract_first()
        next_url = response.urljoin(next_page)#url的合并
        yield scrapy.Request(url=next_url,callback=self.parse)#翻页请求


