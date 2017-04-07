import scrapy
import json

from AospMakefileSpider.items import AospmakefilespiderItem

git_list_urls = []

with open('repo_master.json') as json_data:
    gitList = json.load(json_data)
    for git in gitList:
        git_list_urls.append(git['url'])

android_googlesource = 'https://android.googlesource.com'
baseDir = ''
# baseUrl = android_googlesource + '/platform/system/tools/aidl/+/master'

class RepoSpider(scrapy.Spider):
    name = "git"
    allowed_domains = [ 'android.googlesource.com' ]
    start_urls = git_list_urls

    # def start_requests(self):
    #     yield scrapy.Request(url=baseUrl, callback=self.parse)

    def parse(self, response):
        list = response.css('.FileList-itemLink')
        for item in list:
            name = item.xpath('text()').extract()[0]
            urls = item.xpath('@href').extract()

            if (name.endswith('.mk')) or (name.endswith('.bp')) or (name.endswith('.gradle')):
                # print('catch  remote file = ' + urls[0])
                url = android_googlesource + urls[0]
                fileItem = AospmakefilespiderItem()
                fileItem['url'] = url
                # idx = len(baseUrl)
                # fileItem['path'] = baseDir + url[idx:]
                fileItem['name'] = name
                yield fileItem
            elif "." in name:
                # print('ignore remote file = ' + urls[0])
                continue
            else:
                # print('crawl  remote dir  = ' + urls[0])
                url = android_googlesource + urls[0]
                yield scrapy.Request(url=url, callback=self.parse)
