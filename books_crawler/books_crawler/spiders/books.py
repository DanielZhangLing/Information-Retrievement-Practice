# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
# from selenium import webdriver
# from scrapy.selector import Selector
from scrapy.http import Request
# from time import sleep
# from selenium.common.exceptions import NoSuchElementException

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_url = ['']

    def start_requests(self):
        self.driver = webdriver.Chrome('/Users/LingZhang/Downloads/chromedriver')
        self.driver.get('http://books.toscrape.com')

        sel = Selector(text=self.driver.page_source)
        books = sel.xpath('//h3/a/@href').extract()
        for book in books:
            url = 'http://books.toscrape.com/' + book
            yield Request(url, callback=self.parse_book)
        while True:
            try:
                next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
                sleep(3)
                self.logger.info("sleep for 3 seconds.")
                next_page.click()
                sel = Selector(text=self.driver.page_source)
                books = sel.xpath('//h3/a/@href').extract()
                for book in books:
                    url = 'http://books.toscrape.com/catalogue/' + book
                    yield Request(url, callback=self.parse_book)
            except NoSuchElementException:
                self.logger.info('no more page to load')
                self.driver.quit()
                break
                pass
    def parse_book(self, response):
        pass

    # start_urls = ['http://books.toscrape.com/']
    #
    # rules= (Rule(LinkExtractor(allow=('music'),deny_domains=('google.com')),callback='parse_page', follow=True),)
    # def parse_page(self, response):
    #     yield {'URL': response.url}
