# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy import Item


class API(Item):
    name = Field()
    tags = Field()
    description = Field()
    updated_time = Field()
    pweb_link = Field()
    provider = Field()
    end_point = Field()
    home_page = Field()
    primary_category = Field()
    secondary_category = Field()
    protocol = Field()
    other_option = Field()
    SSL_suport = Field()
    API_Kits = Field()
    API_Forum = Field()
    twitter_Url = Field()
    console_Url = Field()
    authentication_mode = Field()
    differentiators = Field()
    contact_mail = Field()
    developer_support = Field()
    related_to = Field()


class API_Followers(Item):
    api_name = Field()
    followers_list = Field()

class API_Developers(Item):
    api_name = Field()
    developers_list = Field()






