from scrapy import cmdline

from pymongo import MongoClient

import os

import re

if __name__ == '__main__':
    i = 1
    print "Times %d" % (i)
    os.system(r"cd /d D:\Programming\Python\PWebCrawler")
    os.system(r"scrapy crawl pweb")
    db = MongoClient(host="localhost", port=27017)
    collection = db.api.quited_url
    while collection.count() > 0:
        i += 1
        print "Times %d" % (i)
        os.system(r"cd /d D:\Programming\Python\PWebCrawler")
        os.system(r"scrapy crawl pweb")
    print "The Crawler Program Over"

