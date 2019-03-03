# -*- coding: utf-8 -*-
from Cls_Interfaces import *
from Cls_PacketParse import *
from DAL.Cls_PacketInsert_DAL import *
from DAL.Cls_TcpStateInsert_DAL import *
from Cls_IPReputation import *
import threading
import time #şimdilik eklendi silinecek
from Tkinter import *
from pymongo import MongoClient
import datetime #şimdilik eklendi silinecek

def packetParse():
    '''
    _inh_Interface = Cls_Interface()
    lst_myDevices = _inh_Interface.fnc_get_myDevices()

    str_selectDevice = raw_input(">>> Bir interface seciniz >>> ")

    if str_selectDevice in lst_myDevices:
        print "Izlenecek cihaz : " + str_selectDevice
    else:
        print "Girmis oldugunuz " + str_selectDevice + " makinenizde mevcut degil."
        sys.exit()
    '''
    _inh_PacketParse = Cls_PacketParse()
    cap = pcapy.open_live('\Device\NPF_{D30712A8-2060-49A9-A978-D8A919E264D8}', 65536, 1, 0)
    '''Var olan pcap dosyasindan veri okumak icin eklendi kontrol icin'''
    #cap=pcapy.open_offline("ExampleData.pcap")
    _inh_DBConnection = Cls_PacketInsert_DAL()
    _inh_DBSateConnection = Cls_ForSateInsert_DAL()
    while (1):
        now = datetime.datetime.now()
        #print 'Current second parse: %d' % now.second
        (header, packet) = cap.next()

        packet_db_insert = []
        eth_db = {
                    "eth_dest_addr":"",
                    "eth_source_addr":"",
                    "eth_protocol":""
                  }
        ip_db = {
                    "ip_version":"",
                    "ip_header_length":"",
                    "ip_type_of_service":"",
                    "ip_total_length":"",
                    "ip_identification":"",
                    "ip_flags":"",
                    "ip_fragment_offset":"",
                    "ip_time_to_live":"",
                    "ip_protocol":"",
                    "ip_header_checksum":"",
                    "ip_source_addr":"",
                    "ip_dest_addr":""
                }
        tcp_db = {
                    "tcp_source_port":"",
                    "tcp_dest_port":"",
                    "tcp_sequence_number":"",
                    "tcp_ack_number":"",
                    "tcp_data_offset":"",
                    "tcp_reserved":"",
                    "tcp_flags":"",
                    "tcp_window_size":"",
                    "tcp_checksum":"",
                    "tcp_urgent_pointer":""
                }
        udp_db = {
                    "udp_source_port":"",
                    "udp_dest_port":"",
                    "udp_length":"",
                    "udp_checksum":""
                }
        icmp_db = {
                    "icmp_type":"",
                    "icmp_code":"",
                    "icmp_checksum":""
                  }

        eth_db = _inh_PacketParse.fnc_parse_ethHeader(packet)
        #print("ETHERNET parse")

        if _inh_PacketParse.eth_protocol == 8:
            ip_db = _inh_PacketParse.fnc_parse_ipHeader(packet)
            #print("IP parse")

            if _inh_PacketParse.ip_protocol == 6:
                tcp_db = _inh_PacketParse.fnc_parse_tcpHeader(packet)
                #print("TCP parse")
                #print _inh_PacketParse.tcp_flags
                synState = _inh_PacketParse.fnc_insert_syn()
                if synState != False:
                    #print'syn'
                    _inh_DBSateConnection.fnc_db_insert(synState)
                else:
                    synAckState=_inh_PacketParse.fnc_insert_synAck()
                    if synAckState !=False:
                        #print'synAck'
                        _inh_DBSateConnection.fnc_db_insert(synAckState)
                    else:
                        ackState=_inh_PacketParse.fnc_insert_ack()
                        if ackState != False:
                            #print'Ack'
                            _inh_DBSateConnection.fnc_db_insert(ackState)

            if _inh_PacketParse.ip_protocol == 17:
                udp_db = _inh_PacketParse.fnc_parse_udpHeader(packet)
                #print("UDP parse")

            if _inh_PacketParse.ip_protocol == 1:
                icmp_db = _inh_PacketParse.fnc_parse_icmpHeader(packet)
                #print("ICMP parse")

        packet_db_insert = [eth_db, ip_db, tcp_db, udp_db, icmp_db]
        _inh_DBConnection.fnc_db_insert(packet_db_insert)

        client = MongoClient()
        dbState = client.programState
        programState = ([z['program_state'] for z in list(dbState.packets.find({'id': 1}))])
        if (str(programState).replace('[', '').replace(']', '') == '1'):
            break
#Uzun sürsün diye 1 saniyelik delay eklenmiştir döngüye
def ipReputations():
    time.sleep(5)
    ipReputation=Cls_IPReputations()
    client = MongoClient()
    dbState = client.State
    ipCount =dbState.packets.find().count()
    for i in range(1, ipCount):
        #print 'ipreputation working'
        ipdestAddr =' ,'.join([z['ip_dest_addr'] for z in list(dbState.packets.find({'id': i}))])
        ipReputation.fnc_ip_reputation(ipdestAddr)
    db = client.programState
    programState = ([z['program_state'] for z in list(db.packets.find({'id': 1}))])
    if (str(programState).replace('[', '').replace(']', '') != '1'):
        ipReputations()


def terminateApp():
    client = MongoClient()
    db = client.programState

    db.packets.update(
            {'id': 1},
            {
             '$set': {'program_state': 1}
            }
    )
def startApp():
    client = MongoClient()
    db = client.programState
    db.packets.delete_many({})
    db.packets.insert_one(
        {
            'id'           :1,
            'program_state':0
        }
    )
class applicationInterface(object):
    def __init__(self):

        #Açılan pencereyi ayarlar
        self.width=400
        self.height=300
        self.screenWidth=window.winfo_screenwidth()
        self.screenHeight=window.winfo_screenheight()
        self.x=(self.screenWidth-self.width)/2
        self.y = (self.screenHeight - self.height) / 2

        #Başlatma butonu
        self.btnStart = Button(text="Basla", command=main,fg="#FA5858")
        self.btnStart.pack(side=LEFT)
        self.btnStart.config(width=8,height=4)

        #Sonlandırma butonu
        self.btnTerminate = Button(text="Sonlandır", command=terminateApp,fg="#FA5858")
        self.btnTerminate.pack(side=RIGHT)
        self.btnTerminate.config(width=8,height=4)
class myThread (threading.Thread):
    def __init__(self, threadID, name,willUsedFnc):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.willUsedFnc = willUsedFnc

    def run(self):
        if self.willUsedFnc == "packetParse":
            print "Starting " + self.name
            packetParse()
            print "Exiting " + self.name
        elif self.willUsedFnc == "ipReputation":
            print "Starting " + self.name
            ipReputations()
            print "Exiting " + self.name,


def main():
    startApp()
    thread1 = myThread(1, "Thread-1(Parse)", "packetParse")
    thread2 = myThread(2, "Thread-2(ipReputation)", "ipReputation")
    thread1.start()
    thread2.start()
if __name__ == "__main__":
    window = Tk()
    window.tk_setPalette("#2E2E2E")
    interface=applicationInterface()
    window.geometry("%dx%d+%d+%d" % (interface.width, interface.height, interface.x, interface.y))
    mainloop()