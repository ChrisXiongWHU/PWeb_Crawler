from scrapy import signals

from pymongo import MongoClient

from PWebCrawler.url_storage import global_quited_url_queue


class SpiderCloseUrlStatusExtension(object):
    @classmethod
    def from_crawler(cls,crawler):
        ext = cls()
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_closed(self,spider):
        if global_quited_url_queue.__len__() > 0:
            db = MongoClient(host="localhost", port=27017)
            collection = db.api.quited_url
            collection.insert(global_quited_url_queue)



