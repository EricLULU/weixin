from redis import StrictRedis
from pickle import dumps, loads    #序列化的库

class Redis(object):

    def __init__(self):
        self.redis = StrictRedis(host='localhost', port=6379)

    def push(self, url_item):
        self.redis.rpush("weixin", dumps(url_item))              #压入列表
       
    
    def pop(self):
        url_item = loads(self.redis.lpop("weixin"))
        return url_item

    def llen(self):
        return self.redis.llen("weixin") == 0

    def delete(self):
        """
            删除数集合
        """
        if self.redis.exists("weixin"):
            self.redis.delete("weixin")