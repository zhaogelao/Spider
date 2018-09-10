# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from selenium.common.exceptions import TimeoutException
from scrapy.http import HtmlResponse

class SeleniumDownloaderMiddleware(object):

    def __init__(self,timeout):
        self.browser = webdriver.Chrome()#声明浏览器
        self.wait=WebDriverWait(self.browser,timeout)#设置显式等待时间
        self.logger = logging.getLogger(__name__)#关于调试信息

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            timeout=crawler.settings.get('TIMEOUT')
        )

    #用selenium处理request
    def process_request(self, request, spider):
        page = request.meta['page']#获得页码信息
        self.browser.get(request.url)#输入url
        try:
            if page>1:
                inputs = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.form > input')))
                button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div.form > span.btn.J_Submit')))
                inputs.clear()
                inputs.send_keys(page)#输入当前页码
                button.click()#点击按钮
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.items .item')))
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'li.item.active > span'),str(page)))
            #返回Response对象
            return HtmlResponse(url=request.url,status=200,body=self.browser.page_source,request=request,encoding='utf-8')
        except TimeoutException:
            return HtmlResponse(url=request.url,status=500,request=request)
        # self.logger.info(page)
        # return None

    def __del__(self):
        self.browser.close()#类结束的时候，关闭浏览器