import pymongo

class Mongo(object):
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.client.weixin
        self.collection = self.db.AI

    def save(self, data):
        """
            存储到数据库
        """
        if self.collection.insert(data):
            pass
        else:
            print("存储失败")