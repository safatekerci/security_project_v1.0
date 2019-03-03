from pymongo import MongoClient
from Cls_DBConnection import *

class Cls_PsutilInsert_DAL(object):
    def __init__(self):
        self.client = MongoClient()
        self.db_conn = self.client.ConnectionSecurityDB

    def fnc_db_insert(self, psutil_db):
        db_psutil = self.db_conn.OsTrafficColl.insert_one(
        {
            "processID": psutil_db["processID"],
            "localAdd": psutil_db["localAdd"],
            "localAddPort": psutil_db["localAddPort"],
            "remoteAdd": psutil_db["remoteAdd"],
            "remoteAddport": psutil_db["remoteAddport"],
            "processName": psutil_db["processName"],
            "processExePath": psutil_db["processExePath"],
            "processWorkPath": psutil_db["processWorkPath"],
            "protocol": psutil_db["protocol"],
        }
    )