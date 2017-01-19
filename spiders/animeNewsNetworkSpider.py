import scrapy
import re


class ReviewItem(scrapy.Item):
    Name = scrapy.Field()
    Name2 = scrapy.Field()
    Synopsis = scrapy.Field()
    Review = scrapy.Field()
    Good_points = scrapy.Field()
    Bad_points = scrapy.Field()
    Ratings = scrapy.Field()
    

class ReviewsSpider(scrapy.Spider):
    name = "animeNewsNetworkSpider"
    
    def start_requests(self):
        urls = [u"https://www.animenewsnetwork.com/review/archive"]
        for url in urls:
            yield scrapy.Request(url=url, callback = self.get_urls)


    
    def get_urls(self, response):
        
        url_list = response.xpath(u'//*[@id="content-zone"]//ul//@href')
        
        for url in url_list:
            next_page = url.extract()            
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, self.parse)


    def parse(self, response):
        
        table = ' '.join(response.xpath(u'//*[@id="content-zone"]//table//text()').extract())
        yield {
                'Name': response.xpath(u'//*[@id = "content-zone"]//h1//text()').extract(),
                'Name2': response.xpath(u'//*[@id = "content-zone"]//h2//text()').extract(),
                'Synopsis': response.xpath(u'//*[@id = "small-synopsis-area"]//text()').extract(),
                'Review': response.xpath(u'//*[@id = "content-zone"]//*[@class= "text-zone"]')[2].xpath('.//text()').extract(),
                
                'Good_points': response.xpath(u'//*[@id = "content-zone"]//*[@class = "good-points"]/following-sibling::text()').extract_first() , 
                'Bad_points': response.xpath(u'//*[@id = "content-zone"]//*[@class = "bad-points"]/following-sibling::text()').extract_first(),
                'Ratings' : dict(re.findall( r'([\w]+ ?\(?[\w]+[\(\) ]*)\s:\s([ABCDE][+-]?)', table, flags = re.DOTALL))
                }
            
       #table = ' '.join(response.xpath(u'//*[@id="content-zone"]//table//text()').extract())
       # to_yield2 =  dict(re.findall( r'([\w]+ ?\(?[\w]+[\(\) ]*)\s:\s([ABCDE][+-]?)', table, flags = re.DOTALL))
        
        