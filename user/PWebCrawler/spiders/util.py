def item_filled(result_nonextract,item,attribute,do_strip = False):
    if(result_nonextract):
        result_extract = result_nonextract.extract()
        if do_strip:
            item[attribute] = result_extract[0].strip().encode("utf-8")
        else:
            item[attribute] = result_extract[0].encode("utf-8")
    else:
        item[attribute] = None

def api_item_init(item):
    item["name"] = None
    item["primary_category"]= None
    item["secondary_category"]= None
    item["tags"]= None
    item["description"]= None
    item["pweb_link"]= None
    item["updated_time"]= None
    item["provider"]= None
    item["home_page"]= None
    item["end_point"]= None
    item["protocol"]= None
    item["other_option"]= None
    item["SSL_suport"]= None
    item["API_Kits"]= None
    item["API_Forum"]= None
    item["twitter_Url"]= None
    item["console_Url"]= None
    item["developer_support"]= None
    item["authentication_mode"]= None
    item["contact_mail"]= None
    item["differentiators"]= None
    item["related_to"]= None

def api_followers_init(item):
    item["api_name"] = None
    item["followers_list"] = None

def api_developers_init(item):
    item["api_name"] = None
    item["developers_list"] = None

def item_filed_from_dict(item,dict):
    for key,value in dict.items():
        item[key] = value
