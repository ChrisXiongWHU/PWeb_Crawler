# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from PWebCrawler.items import API
from PWebCrawler.items import API_Followers
from PWebCrawler.items import API_Developers

from spiders.process_util import Process_Util

class PWebPipeline(object):
    process_util = Process_Util()
    def process_item(self,item,spider):
        # print item
        if isinstance(item,API):
            self.process_util.api_summary_process(item)
        elif isinstance(item,API_Followers):
            self.process_util.api_follower_process(item)
        elif isinstance(item,API_Developers):
            self.process_util.api_developer_process(item)




