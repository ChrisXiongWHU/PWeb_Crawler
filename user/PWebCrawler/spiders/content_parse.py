from scrapy import Selector
from PWebCrawler.spiders.util import item_filled


class API_Summary_Parse(object):
    xpath_name = '//div[@class="node-header"]/h1/text()'
    xpath_description = '//div[@class="api_description tabs-header_description"]/text()'
    xpath_tags = '//div[@class="tags"]/a/text()'
    xpath_summary_field = '//div[@class="section specs"]/div[@class="field"]'

    def set_response(self,response):
        self.sel = Selector(response)

    def parse(self,item):
        name = self.sel.xpath(self.xpath_name).extract()[0].encode("utf-8")
        item["name"] = name.rstrip(" API")
        description = self.sel.xpath(self.xpath_description)
        item_filled(description,item,"description",True)

        tags = self.sel.xpath(self.xpath_tags)
        tags_str = ""
        if tags:
            tags = tags.extract()
            for tag in tags:
                tags_str += tag + ","
            tags_str = tags_str.rstrip(",")
        else:
            tags_str = None

        item["tags"] = tags_str

        summary_field = self.sel.xpath(self.xpath_summary_field)

        for summary_each_field in summary_field:
            label = summary_each_field.xpath('./label/text()').extract()[0].strip()
            summary_content = summary_each_field.xpath('./span/text()|./span/*/text()').extract()
            content = ''.join(summary_content)
            field = self.__switch_label(label)
            item[field] = content.encode("utf-8")
        return item

    def __switch_label(self,label):
        labels = {"API Provider":"provider",
                  "API Endpoint":"end_point",
                  "API Homepage":"home_page",
                  "Primary Category":"primary_category",
                  "Secondary Categories":"secondary_category",
                  "Protocol / Formats":"protocol",
                  "Other options":"other_option",
                  "SSL Support":"SSL_suport",
                  "API Kits":"API_Kits",
                  "API Forum":"API_Forum",
                  "Twitter Url":"twitter_Url",
                  "Developer Support":"developer_support",
                  "Console URL":"console_Url",
                  "Authentication Mode":"authentication_mode",
                  "Differentiators":"differentiators",
                  "Contact Email":"contact_mail",
                  "Related to?":"related_to"}
        return labels[label]

class API_Followers_Parse(object):
    xpath_user = '//a[@class="username"]'

    def set_response(self, response):
        self.sel = Selector(response)
        self.response = response

    def parse(self,item):
        user_list = self.sel.xpath(self.xpath_user)
        this_page_list = item.get("followers_list", None)
        need_access = self.response.meta.get("need_access",[])
        if user_list:
            if this_page_list is None:
                this_page_list = []
            for user in user_list:
                link = user.xpath('./@href').extract()[0].encode("utf-8")
                name = user.xpath('./text()').extract()[0].encode("utf-8")
                if name.endswith("..."):
                    need_access.append(link)
                else:
                    user = {"name": name, "link": link}
                    this_page_list.append(user)
        item["followers_list"] = this_page_list
        return need_access

class API_Developers_Parse(object):
    xpath_user = '//a[@class="username"]'

    def set_response(self, response):
        self.sel = Selector(response)
        self.response = response

    def parse(self, item):
        user_list = self.sel.xpath(self.xpath_user)
        this_page_list = item.get("developers_list",None)
        need_access = self.response.meta.get("need_access", [])
        if user_list:
            if this_page_list is None:
                this_page_list = []
            for user in user_list:
                link = user.xpath('./@href').extract()[0].encode("utf-8")
                name = user.xpath('./text()').extract()[0].encode("utf-8")
                if name.endswith("...") and link not in need_access:
                    need_access.append(link)
                else:
                    user = {"name": name, "link": link}
                    if user not in this_page_list:
                        this_page_list.append(user)
        item["developers_list"] = this_page_list
        return need_access
















