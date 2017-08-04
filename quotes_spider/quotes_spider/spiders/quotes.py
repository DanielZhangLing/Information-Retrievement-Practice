# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

from quotes_spider.items import QuotesSpiderItem


class QuotesSpider(Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()
        return FormRequest.from_response(response, formdata={
            'csrf_token': token,
            'password': 'foobar',
            'username': 'foobar',
        },
                                         callback=self.scrape_home_page)

    def scrape_home_page(self, response):
        # open_in_browser(response)
        # l = ItemLoader(item=QuotesSpiderItem(), response=response)
        h1_tag = response.xpath('//h1/a/text()').extract_first()
        tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()
        # l._add_value('h1_tag', h1_tag)
        # l.add_value('tags', tags)
        print(h1_tag)
        print(tags)
        # return l.load_item()
        # yield {'H1 Tag': h1_tag, 'Tags': tags}
        # quotes = response.xpath('//*[@class="quote"]')
        # for quote in quotes:
        #     text = quote.xpath('.//*[@class="text"]/text()').extract_first()
        #     author = quote.xpath('.//*[@itemprop="author"]/text()').extract_first()
        #     tags = quote.xpath('.//*[@class="tag"]/text()').extract()
        #     yield {'Text': text, "Author": author, "Tags": tags}
        # next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        # absolute_next_page_url = response.urljoin(next_page_url)
        # yield Request(absolute_next_page_url, callback=self.parse)
