import scrapy

from AospRepoSpider.items import AosprepospiderItem

domain = 'https://android.googlesource.com'
baseUrl = domain + '/tools/repo/+refs'

class RepoSpider(scrapy.Spider):
    name = "repo"
    allowed_domains = [ domain ]

    def start_requests(self):
        yield scrapy.Request(url=baseUrl, callback=self.parse)

    def parse(self, response):
        list = response.css('.RefList-item')
        repoItems = []
        for item in list:
            name = item.xpath('a/text()').extract()[0]
            urls = item.xpath('a/@href').extract()
            url = domain + urls[0]
            repoItem = AosprepospiderItem()
            repoItem['name'] = name
            repoItem['url'] = url
            repoItems.append(repoItem)
        return repoItems
