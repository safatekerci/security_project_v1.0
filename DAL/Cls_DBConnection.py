from pymongo import MongoClient

class Cls_DBConnection(object):

    def fnc_DBConnection(self,p_dbCollectionName):
        self.client = MongoClient()
        self.db = self.client.p_dbCollectionName