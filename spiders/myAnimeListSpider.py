# -*- coding: utf-8 -*-
import scrapy
import re

class MyanimelistspiderSpider(scrapy.Spider):
    name = "myAnimeListSpider"
    start_urls = [u"https://myanimelist.net/reviews.php?t=anime"]



    def parse(self, response):
        for review in  response.xpath(r'//*[@id="content"]/div'):
            
            review_text = ' '.join(review.xpath(r'./div[3]/text()').extract())
            review_text += ' '.join(review.xpath(r'./div[3]/span//text()').extract())
            
            table_text =  ''.join(review.xpath(r'.//table/tr//text()').extract())
            
            yield {
                   #'review_text': ' '.join(review.xpath(r'./div[3]//text()').extract()),
                    'Name': review.xpath(r'./div/a//text()').extract_first(),
                    'review_text': review_text,
                    'Rating': review.re(r'Overall Rating.*?(\d{1,2})'),
                    'Story': re.findall(r'Story.*?(\d{1,2})', table_text, flags =re.DOTALL),
                    'Animation': re.findall(r'Animation.*?(\d{1,2})', table_text, flags =re.DOTALL),
                    'Sound': re.findall(r'Sound.*?(\d{1,2})', table_text, flags =re.DOTALL),
                    'Character': re.findall(r'Character.*?(\d{1,2})', table_text, flags =re.DOTALL),
                    'Enjoyment': re.findall(r'Enjoyment.*?(\d{1,2})', table_text, flags =re.DOTALL),
            }
        
            
            next_page = response.xpath(r'//a[contains(text(),"Next")]/@href').extract_first()
            # next_page = response.xpath(r'//a[text() = "Next "]/@href').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, self.parse)
            
            