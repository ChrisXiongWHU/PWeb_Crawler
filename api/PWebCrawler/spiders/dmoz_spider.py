# -*- coding:utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from PWebCrawler.items import API
from PWebCrawler.items import API_Followers
from PWebCrawler.items import API_Developers


from scrapy import Request

from PWebCrawler.spiders.content_parse import API_Summary_Parse
from PWebCrawler.spiders.content_parse import API_Followers_Parse
from PWebCrawler.spiders.content_parse import API_Developers_Parse

from PWebCrawler.spiders.util import item_filled
from PWebCrawler.spiders.util import item_filed_from_dict
from PWebCrawler.spiders.util import api_item_init
from PWebCrawler.spiders.util import api_followers_init
from PWebCrawler.spiders.util import api_developers_init


from pymongo import MongoClient

class PWebSpider(Spider):
    name = "pweb"
    allowed_domains = ["www.programmableweb.com"]
    start_urls = [
        "http://www.programmableweb.com/apis/directory"
    ]
    base_url = "http://www.programmableweb.com"

    page_count = 0


    api_summary_parse_util = API_Summary_Parse()
    api_watchlist_parse_util = API_Followers_Parse()
    api_developers_parse_util = API_Developers_Parse()

    #恢复上次运行失败的request
    def start_requests(self):
        requests = []
        items = []
        db = MongoClient(host="localhost", port=27017)
        collection = db.api.quited_url
        for item in collection.find():
            items.append(item)
        collection.remove()
        if items.__len__() > 0:
            for item in items:
                url = item["url"].encode("utf-8")
                types = item["type"]
                item_each = item["item"]
                need_access_each = item["need_access"]
                if types == 'api_page':
                    api = API()
                    api_item_init(api)
                    if item_each is not None:
                        item_filed_from_dict(api, item_each)
                    requests.append(Request(url=url,callback=self.parse,meta={'type':'api_page','item':api},dont_filter=True))
                elif types == 'followers_page':
                    api_followers = API_Followers()
                    api_followers_init(api_followers)
                    if item_each is not None:
                        item_filed_from_dict(api_followers, item_each)
                    requests.append(Request(url=url,callback=self.api_followers_parse,
                                            meta={'type':'followers_page','item':api_followers,'need_access':need_access_each},dont_filter=True))
                elif types == 'developers_page':
                    api_developers = API_Developers()
                    api_developers_init(api_developers)
                    if item_each is not None:
                        item_filed_from_dict(api_developers, item_each)
                    requests.append(Request(url=url,callback=self.api_developers_parse,
                                            meta={'type':'developers_page','item':api_developers,'need_access':need_access_each},dont_filter=True))
                elif types == 'api_summary':
                    api = API()
                    api_item_init(api)
                    if item_each is not None:
                        item_filed_from_dict(api, item_each)
                    requests.append(Request(url=url,callback=self.api_summary_parse,meta={'type':'api_summary','item':api},dont_filter=True))
                elif types == 'user_page_f':
                    api_followers = API_Followers()
                    api_followers_init(api_followers)
                    if item_each is not None:
                        item_filed_from_dict(api_followers, item_each)
                    requests.append(Request(url=url, callback=self.user_exceed_parse,
                                        meta={'type': 'user_page_f', 'item': api_followers,'need_access':need_access_each},dont_filter=True))
                elif types == 'user_page_d':
                    api_developers = API_Developers()
                    api_developers_init(api_developers)
                    if item_each is not None:
                        item_filed_from_dict(api_developers, item_each)
                    requests.append(Request(url=url, callback=self.user_exceed_parse,
                                            meta={'type': 'user_page_d', 'item': api_developers,'need_access':need_access_each},dont_filter=True))
        else:
            # requests.append(Request(url="http://www.programmableweb.com/api/google-app-engine",callback=self.api_summary_parse,dont_filter=True))
            requests.append(Request(url="http://www.programmableweb.com/apis/directory",meta={'type':'api_page'},callback=self.parse,dont_filter=True))

        return requests

    def parse(self, response):


        sel = Selector(response)
        api_url_list = sel.xpath('//td[@class="views-field views-field-title col-md-3"]/a/@href').extract()
        for api_url in api_url_list:
            updated_date = sel.xpath('//td/a[@href="'+api_url+'"]/../following-sibling::td[@class="views-field views-field-created"]/text()')
            api_item = API()
            api_item_init(api_item)
            api_item['pweb_link'] = self.base_url+api_url.strip().encode("utf-8")
            item_filled(updated_date,api_item,'updated_time',True)
            yield Request(url=self.base_url+api_url,callback=self.api_summary_parse,meta={'item':api_item,'type':'api_summary'},dont_filter=True)

        next_page_urls = sel.xpath('//a[@title="Go to next page"]/@href')
        if next_page_urls:
            next_page_url = next_page_urls.extract()[0]
            yield Request(self.base_url+next_page_url,self.parse,meta={'type':'api_page'},dont_filter=True)

    def api_summary_parse(self,response):
        api_item = response.meta.get('item',API())
        self.api_summary_parse_util.set_response(response)
        self.api_summary_parse_util.parse(api_item)

        api_followers_item = API_Followers()
        api_followers_init(api_followers_item)
        api_followers_item["api_name"] = api_item["name"]

        api_developers_item = API_Developers()
        api_developers_init(api_developers_item)
        api_developers_item["api_name"] = api_item["name"]

        yield api_item
        yield Request(url=response.url+"/followers",meta={'item':api_followers_item,'type':'followers_page'},callback=self.api_followers_parse,dont_filter=True)
        yield Request(url=response.url+"/developers",meta={'item':api_developers_item,'type':'developers_page'},callback=self.api_developers_parse,dont_filter=True)

    def api_followers_parse(self,response):
        sel = Selector(response)
        api_followers_item = response.meta['item']
        self.api_watchlist_parse_util.set_response(response)
        need_access = self.api_watchlist_parse_util.parse(api_followers_item)
        # print "\n\n\nFOLLOWERS"
        # print need_access
        # print "\n\n\n"
        xpath_next_page = '//a[@class="pw_load_more"]/@href'
        next_page = sel.xpath(xpath_next_page)
        if next_page:
            next_page_url = next_page.extract()[0]
            if need_access is not None and need_access.__len__() > 0:
                yield Request(url=self.base_url + next_page_url,
                              meta={'item': api_followers_item, 'type': 'followers_page',
                                    'need_access':need_access},
                              callback=self.api_followers_parse,dont_filter=True)
            else:
                yield Request(url=self.base_url + next_page_url,
                              meta={'item': api_followers_item, 'type': 'followers_page'},
                              callback=self.api_followers_parse,dont_filter=True)
        else:
            if need_access is not None and need_access.__len__() >0:
                link = need_access[0]
                need_access.pop(0)
                yield Request(url=self.base_url + link,
                              meta={'item': api_followers_item, 'type': 'user_page_f',
                                    'need_access': need_access},
                              callback=self.user_exceed_parse,dont_filter=True)
            else:
                yield api_followers_item



    def api_developers_parse(self,response):
        sel = Selector(response)
        api_developers_item = response.meta['item']
        self.api_developers_parse_util.set_response(response)
        need_access = self.api_developers_parse_util.parse(api_developers_item)
        # print "\n\n\nDEVELOPERS"
        # print need_access
        # print "\n\n\n"
        xpath_next_page = '//a[@class="pw_load_more"]/@href'
        next_page = sel.xpath(xpath_next_page)
        if next_page:
            next_page_url = next_page.extract()[0]
            if need_access is not None and need_access.__len__() > 0:
                yield Request(url=self.base_url + next_page_url,
                              meta={'item': api_developers_item , 'type': 'developers_page',
                                    'need_access': need_access},
                              callback=self.api_developers_parse,dont_filter=True)
            else:
                yield Request(url=self.base_url + next_page_url,
                              meta={'item': api_developers_item , 'type': 'developers_page'},
                              callback=self.api_developers_parse,dont_filter=True)
        else:
            if need_access is not None and need_access.__len__() > 0:
                link = need_access[-1]
                need_access.pop()
                yield Request(url=self.base_url + link,
                              meta={'item': api_developers_item , 'type': 'user_page_d',
                                    'need_access': need_access},
                              callback=self.user_exceed_parse,dont_filter=True)
            else:
                yield api_developers_item

    def user_exceed_parse(self,response):
        # print "\n\n\nUSER_EXCEED"
        # print response.meta["need_access"]
        # print "\n\n\n"
        sel = Selector(response)
        user_name = sel.xpath('//div[@class="about pull-left"]/div[@class="field"][1]/span/text()')[0].extract().encode("utf-8")
        item = response.meta["item"]
        type = response.meta["type"]
        if type == "user_page_f":
            followers_list = item.get("followers_list",[])
            link = "/" + "/".join(response.url.split("/")[-2:])
            user = {"name":user_name,"link":link}
            followers_list.append(user)
            item["followers_list"] = followers_list
        elif type == "user_page_d":
            developers_list = item.get("developers_list", [])
            link = "/" + "/".join(response.url.split("/")[-2:])
            user = {"name": user_name, "link": link}
            developers_list.append(user)
            item["developers_list"] = developers_list

        need_access = response.meta.get("need_access", [])
        if need_access is not None and need_access.__len__() > 0:
            if item["api_name"] == "GeoNames":
                print need_access
            next_link = need_access[-1]
            need_access.pop()
            if type == "user_page_f":
                yield Request(url=self.base_url + next_link,
                              meta={'item': item, 'type': 'user_page_f',
                                    'need_access': need_access},
                              callback=self.user_exceed_parse,dont_filter=True)
            elif type == "user_page_d":
                yield Request(url=self.base_url + next_link,
                              meta={'item': item, 'type': 'user_page_d',
                                    'need_access': need_access},
                              callback=self.user_exceed_parse,dont_filter=True)
        else:
            if item["api_name"] == "GeoNames":
                print item
            yield item





