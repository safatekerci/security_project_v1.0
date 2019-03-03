import pcapy
import socket
from _winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, OpenKey, QueryValueEx
import netifaces
import sys
from struct import *
import pymongo
from pymongo import *
from netifaces import *

class Cls_PacketParse(object):

    def __init__(self):
        #### ethernet protocol variables ####
        self.eth_header = ""
        self.eth_protocol = ""
        self.eth_dest_addr = ""
        self.eth_source_adr = ""
        self.eth_dict = {}

        #### ip protocol variables ####
        self.ip_header = ""
        self.ip_version = ""
        self.ip_header_length = ""
        self.ip_type_of_service = ""
        self.ip_total_length = ""
        self.ip_identification = ""
        self.ip_flags = ""
        self.ip_fragment_offset = ""
        self.ip_time_to_live = ""
        self.ip_protocol = ""
        self.ip_header_checksum = ""
        self.ip_source_addr = ""
        self.ip_dest_addr = ""
        self.ip_data = ""
        self.ip_dict = {}

        #### tcp protocol variables ####
        self.tcp_header = ""
        self.tcp_source_port = ""
        self.tcp_dest_port = ""
        self.tcp_sequence_number = ""
        self.tcp_ack_number = ""
        self.tcp_data_offset = ""
        self.tcp_reserved = ""
        self.tcp_flags = ""
        self.tcp_window_size = ""
        self.tcp_checksum = ""
        self.tcp_urgent_pointer = ""
        self.tcp_data = ""
        self.tcp_dict = {}

        #### udp protocol variables ####
        self.udp_header = ""
        self.udp_source_port = ""
        self.udp_dest_port = ""
        self.udp_length = ""
        self.udp_checksum = ""
        self.udp_dict = {}

        #### icmp protocol variables ####
        self.icmp_header = ""
        self.icmp_type = ""
        self.icmp_code = ""
        self.icmp_checksum = ""
        self.icmp_restOfHeader = ""
        self.icmp_dict = {}

        #### state islemi icin ####
        self.myIp = ' ,'.join([i['addr'] for i in ifaddresses('{D30712A8-2060-49A9-A978-D8A919E264D8}').setdefault(AF_INET, [{'addr': 'No IP addr'}])])
        self.forStateValue = {}
        self.count = 0
        self.syn_packet={}
        self.syn_ack_packet={}
        self.ack_packet={}
    def fnc_convert_eth_addr(self,eth_add):
        eth_add = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(eth_add[0]), ord(eth_add[1]), ord(eth_add[2]), ord(eth_add[3]), ord(eth_add[4]), ord(eth_add[5]))
        return eth_add

    def fnc_parse_ethHeader(self, packet):
        if len(str(packet)) > 14:
            self.eth_header = unpack('!6s6sH', packet[:14])  # separate ethernet header
            self.eth_dest_addr = self.fnc_convert_eth_addr(self.eth_header[0])
            self.eth_source_adr = self.fnc_convert_eth_addr(self.eth_header[1])
            self.eth_protocol = socket.ntohs(self.eth_header[2])
            self.eth_dict = {
                             "eth_dest_addr"    :self.eth_dest_addr,
                             "eth_source_addr"  :self.eth_source_adr,
                             "eth_protocol"     :self.eth_protocol
                            }
            return self.eth_dict
        else:
            return False
    def fnc_parse_ipHeader(self, packet):
        self.ip_header = unpack('!BBHHHBBH4s4s', packet[14:34])
        self.ip_version =  bin(self.ip_header[0]).replace('b','')[:4] #tr(int(bin(self.ip_header[0])[2:].zfill(8)[:4], 2))
        self.ip_header_length = int(bin(self.ip_header[0]).replace('b','')[4:8],2) * 4  #self.ip_header[0] & 0x0F
        self.ip_type_of_service = self.ip_header[1]
        self.ip_total_length = self.ip_header[2]
        self.ip_identification = self.ip_header[3]
        self.ip_flags = bin(self.ip_header[4]).replace('b','')[:3] #str(int(bin(self.ip_header[4])[2:].zfill(8)[:3], 2))#self.ip_header[4] & 0xE000 >> 13
        self.ip_fragment_offset = bin(self.ip_header[4]).replace('b','')[3:] #str(int(bin(self.ip_header[4])[2:].zfill(8)[4:], 2))
        self.ip_time_to_live = self.ip_header[5]
        self.ip_protocol = self.ip_header[6]
        self.ip_header_checksum = self.ip_header[7]
        self.ip_source_addr = socket.inet_ntoa(self.ip_header[8]);
        self.ip_dest_addr = socket.inet_ntoa(self.ip_header[9]);
        self.ip_dict = {
                        "ip_version"        :self.ip_version,
                        "ip_header_length"  :self.ip_header_length,
                        "ip_type_of_service":self.ip_type_of_service,
                        "ip_total_length"   :self.ip_total_length,
                        "ip_identification" :self.ip_identification,
                        "ip_flags"          :self.ip_flags,
                        "ip_fragment_offset":self.ip_fragment_offset,
                        "ip_time_to_live"   :self.ip_time_to_live,
                        "ip_protocol"       :self.ip_protocol,
                        "ip_header_checksum":self.ip_header_checksum,
                        "ip_source_addr"    :self.ip_source_addr,
                        "ip_dest_addr"      :self.ip_dest_addr
                        }
        return self.ip_dict

    def fnc_parse_tcpHeader(self, packet):
        self.tcp_header = unpack('!HHLLHHHH', packet[34:54])
        self.tcp_source_port = self.tcp_header[0]
        self.tcp_dest_port = self.tcp_header[1]
        self.tcp_sequence_number = self.tcp_header[2]
        self.tcp_ack_number = self.tcp_header[3]
        self.tcp_data_offset = bin(self.tcp_header[4]).replace('b','')[:4] #bin(self.tcp_header[4])[2:].zfill(8)[:4]
        self.tcp_reserved = bin(self.tcp_header[4]).replace('b','')[4:10] #bin(self.tcp_header[4])[2:].zfill(8)[4:10]
        self.tcp_flags = bin(self.tcp_header[4]).replace('b','')[10:] #bin(self.tcp_header[4])[2:].zfill(8)[10:16]
        self.tcp_window_size = self.tcp_header[5]
        self.tcp_checksum = self.tcp_header[6]
        self.tcp_urgent_pointer = self.tcp_header[7]
        self.tcp_dict = {
                         "tcp_source_port"      :self.tcp_source_port,
                         "tcp_dest_port"        :self.tcp_dest_port,
                         "tcp_sequence_number"  :self.tcp_sequence_number,
                         "tcp_ack_number"       :self.tcp_ack_number,
                         "tcp_data_offset"      :self.tcp_data_offset,
                         "tcp_reserved"         :self.tcp_reserved,
                         "tcp_flags"            :self.tcp_flags,
                         "tcp_window_size"      :self.tcp_window_size,
                         "tcp_checksum"         :self.tcp_checksum,
                         "tcp_urgent_pointer"   :self.tcp_urgent_pointer
                        }
        return self.tcp_dict

    def fnc_parse_udpHeader(self, packet):
        self.udp_header = unpack('!HHHH', packet[34:42])
        self.udp_source_port = self.udp_header[0]
        self.udp_dest_port = self.udp_header[1]
        self.udp_length = self.udp_header[2]
        self.udp_checksum = self.udp_header[3]
        self.udp_dict = {
                         "udp_source_port"  :self.udp_source_port,
                         "udp_dest_port"    :self.udp_dest_port,
                         "udp_length"       :self.udp_length,
                         "udp_checksum"     :self.udp_checksum
                        }
        return self.udp_dict

    def fnc_parse_icmpHeader(self, packet):
        self.icmp_header = unpack('!BBH', packet[34:38])
        self.icmp_type = self.icmp_header[0]
        self.icmp_code = self.icmp_header[1]
        self.icmp_checksum = self.icmp_header[2]
        self.icmp_dict = {
                          "icmp_type"       :self.icmp_type,
                          "icmp_code"       :self.icmp_code,
                          "icmp_checksum"   :self.icmp_checksum
                         }
        return self.icmp_dict

    #Syn + Ack paket insert
    def fnc_insert_synAck(self):
        #myIp = ' ,'.join([i['addr'] for i in ifaddresses('{D30712A8-2060-49A9-A978-D8A919E264D8}').setdefault(AF_INET, [{'addr': 'No IP addr'}])])

        if self.ip_dest_addr == self.myIp and self.tcp_flags == '0010010':
            self.syn_ack_packet={
                                "packet_type"              :"synAck",
                                "id"                       : self.count,
                                "ip_source_addr"           : self.ip_dest_addr,
                                "ip_dest_addr"             : self.ip_source_addr,
                                "synPacket_sequence_num"   : int(self.tcp_ack_number) - 1,
                                "synAckPacket_sequence_num": self.tcp_sequence_number,
                                "ackPacket_ack_num"        : "",
                                "tcp_state"                : "0",
                                "host_name"                : "",
                                "ip_reputation"            : "",
                                "dns_name"                 : ""
                                }
            return self.syn_ack_packet
        else:
            return False;


    # Ack paket insert
    def fnc_insert_ack(self):
        #myIp = ' ,'.join([i['addr'] for i in ifaddresses('{D30712A8-2060-49A9-A978-D8A919E264D8}').setdefault(AF_INET, [{'addr': 'No IP addr'}])])
        if self.ip_source_addr == self.myIp and self.tcp_flags == '010000':
            self.ack_packet={
                            "packet_type"              : "ack",
                            "id"                       : self.count,
                            "ip_source_addr"           : self.ip_source_addr,
                            "ip_dest_addr"             : self.ip_dest_addr,
                            "synAckPacket_sequence_num": int(self.tcp_ack_number) - 1,
                            "ackPacket_ack_num"        : self.tcp_ack_number,
                            "synPacket_sequence_num"   : "",
                            "tcp_state"                : "1",
                            "host_name"                : "",
                            "ip_reputation"            : "",
                            "dns_name"                 : ""
                            }
            return self.ack_packet
        else:
            return False;

    #Syn paket insert
    def fnc_insert_syn(self):
        #myIp = ' ,'.join([i['addr'] for i in ifaddresses('{D30712A8-2060-49A9-A978-D8A919E264D8}').setdefault(AF_INET, [{'addr': 'No IP addr'}])])
        if self.ip_source_addr == self.myIp and self.tcp_flags == '0000010':
            self.count = self.count + 1
            self.syn_packet={
                             "packet_type"               : "syn",
                             "id"                        : self.count,
                             "ip_source_addr"            : self.ip_source_addr,
                             "ip_dest_addr"              : self.ip_dest_addr,
                             "synPacket_sequence_num"    : self.tcp_sequence_number,
                             "synAckPacket_sequence_num" : '',
                             "ackPacket_ack_num"         : '',
                             "tcp_state"                 : "0",
                             "host_name"                 : "",
                             "ip_reputation"             : "",
                             "dns_name"                  : ""
                            }
            return self.syn_packet
        else:
            return False;

