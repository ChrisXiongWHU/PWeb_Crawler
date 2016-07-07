from pymongo import MongoClient



class Process_Util(object):
    def api_summary_process(self, item):
        db = MongoClient(host="localhost",port=27017)
        collection = db.api.api_summary
        collection.insert(dict(item))

    def api_follower_process(self, item):
        db = MongoClient(host="localhost",port=27017)
        collection = db.api.api_followers
        collection.insert(dict(item))

    def api_developer_process(self, item):
        db = MongoClient(host="localhost",port=27017)
        collection = db.api.api_developers
        collection.insert(dict(item))


            # def api_summary_process(self,item):
    #     db = connect(host="localhost",user="root",passwd="xrb19961119",db="api")
    #     api_summary_table = "api_summary"
    #     cursor = db.cursor()
    #
    #     sql = "INSERT INTO " + api_summary_table + " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #
    #
    #     try:
    #         cursor.execute(sql, (item["name"], item["primary_category"], item["secondary_category"],
    #                              item["tags"], item["description"], item["pweb_link"],
    #                              item["updated_time"], item["provider"], item["home_page"],
    #                              item["end_point"], item["protocol"], item["other_option"],
    #                              item["SSL_suport"], item["API_Kits"], item["API_Forum"],
    #                              item["twitter_Url"], item["console_Url"], item["developer_support"],
    #                              item["authentication_mode"], item["contact_mail"], item["differentiators"],
    #                              item["related_to"]))
    #         db.commit()
    #     except:
    #         db.rollback()
    #     finally:
    #         cursor.close()
    #         db.close()
    #
    # def api_follower_process(self,item):
    #     db = connect(host="localhost", user="root", passwd="xrb19961119", db="api")
    #     api_follower_table = "api_followers"
    #     cursor = db.cursor()
    #
    #     sql = "INSERT INTO " + api_follower_table + " VALUES(%s,%s)"
    #
    #     args = []
    #     followers = item["followers_list"]
    #     api_name = item["api_name"]
    #     if followers:
    #         for follower in followers:
    #             touple = (api_name, follower)
    #             args.append(touple)
    #     else:
    #         args = None
    #
    #     try:
    #         cursor.executemany(sql,args)
    #         db.commit()
    #     except:
    #         db.rollback()
    #     finally:
    #         cursor.close()
    #         db.close()
    #
    # def api_developer_process(self,item):
    #     db = connect(host="localhost", user="root", passwd="xrb19961119", db="api")
    #     api_developer_table = "api_developer"
    #     cursor = db.cursor()
    #
    #     sql = "INSERT INTO " + api_developer_table + " VALUES(%s,%s)"
    #
    #     args = []
    #     developers = item["developers_list"]
    #     api_name = item["api_name"]
    #     if developers:
    #         for developer in developers:
    #             touple = (api_name, developer)
    #             args.append(touple)
    #     else:
    #         args = None
    #     try:
    #         cursor.executemany(sql, args)
    #         db.commit()
    #     except:
    #         db.rollback()
    #     finally:
    #         cursor.close()
    #         db.close()
    #






