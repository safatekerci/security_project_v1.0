# -*- coding: utf-8 -*-
from  pymongo import MongoClient
import socket

class Cls_IPReputations(object):
    def __init__(self):
        self.client = MongoClient()
        self.connSecurity = self.client.BlacListDB
        self.ipRep_dict = {}
    def fnc_IPReuputation(self,ackState):

        isHave = self.connSecurity.IPList.find({'badIP': ackState["ip_dest_addr"]}).count()
        try:
            hostNAme = socket.gethostbyaddr(ackState["ip_dest_addr"])
        except:
            hostNAme = "Bulunamadı"

        if isHave != 0:
            ackState["ip_reputation"] = "Tehlikeli"
            badIpQueryUrl=([z['url'] for z in list(self.connSecurity.IPList.find({'badIP': ackState["ip_dest_addr"]}))])
        else:
            ackState["ip_reputation"] = "Güvenli"
            badIpQueryUrl=""
        ackState["host_name"] = hostNAme[0]
        ackState["dns_name"] = badIpQueryUrl

        print ackState
        print 1000 * '-'

        return ackState
