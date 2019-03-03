# -*- coding: utf-8 -*-
from datetime import datetime
from pymongo import MongoClient
import urllib2, threading, time

class Cls_BlackList(object):
    def __init__(self):
        self.lstQueryURL = [
                # TOR
                ('http://torstatus.blutmagie.de/ip_list_exit.php/Tor_ip_list_EXIT.csv',
                 'is not a TOR Exit Node',
                 'is a TOR Exit Node',
                 False)
         ]
        self.client = MongoClient()
        self.db_conn = self.client.BlackListDB

    def fnc_get_html_content(self,url):
        try:
            request = urllib2.Request(url)
            html_content = urllib2.build_opener().open(request).read()
            return html_content

        except Exception, error:
            return False

    def main(self):
        #time.sleep(180000)
        threading.Timer(30.0, self.main).start()

        for url, succ, fail, mal in self.lstQueryURL:
            if self.fnc_get_html_content(url):
                html_content =  self.fnc_get_html_content(url)
                badIPList = html_content.split("\n")
                id = 1

                for badIP in badIPList:
                    badIP = badIP.split("#")[0]
                    exist = self.db_conn.IPList.find({'badIP': badIP}).count()

                    if exist == 0:
                        db_packet = self.db_conn.IPList.insert_one(
                            {
                                "id":id,
                                "badIP": badIP,
                                "ip_update_date": datetime.now().strftime('%H:%M:%S.%f %d/%m/%Y'),
                                "url":url
                            }
                        )
                        id += 1

if __name__ == "__main__":
    inh_ = Cls_BlackList()
    inh_.main()