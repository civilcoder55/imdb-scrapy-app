# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?groups=top_250&sort=user_rating', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"), process_request='set_user_agent')
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title': response.xpath("//div[contains(@class, 'TitleBlock__TitleContainer')]/h1/text()").get(),
            'year': response.xpath("(//li[@class='ipc-inline-list__item']/a/text())[1]").get(),
            'duration': response.xpath("normalize-space(//li[@class='ipc-inline-list__item']/text())").get(),
            'genre': response.xpath("((//div[@class='ipc-metadata-list-item__content-container'])[13])//a/text()").getall(),
            'rating': response.xpath("//span[contains(@class,'AggregateRatingButton__RatingScore')]//text()").get(),
            'movie_url': response.url
        }
