from pymongo import MongoClient
from Cls_DBConnection import *

class Cls_PacketInsert_DAL(object):
    def __init__(self):
        self.client = MongoClient()
        self.db_conn = self.client.ConnectionSecurityDB

        self.p_eth_protocol = ""
        self.p_eth_dest_addr = ""
        self.p_eth_source_addr = ""

        self.p_ip_header = ""
        self.p_ip_version = ""
        self.p_ip_header_length = ""
        self.p_ip_type_of_service = ""
        self.p_ip_total_length = ""
        self.p_ip_identification = ""
        self.p_ip_flags = ""
        self.p_ip_fragment_offset = ""
        self.p_ip_time_to_live = ""
        self.p_ip_protocol = ""
        self.p_ip_header_checksum = ""
        self.p_ip_source_addr = ""
        self.p_ip_dest_addr = ""

        self.p_tcp_source_port = ""
        self.p_tcp_dest_port = ""
        self.p_tcp_sequence_number = ""
        self.p_tcp_ack_number = ""
        self.p_tcp_data_offset = ""
        self.p_tcp_reserved = ""
        self.p_tcp_flags = ""
        self.p_tcp_window_size = ""
        self.p_tcp_checksum = ""
        self.p_tcp_urgent_pointer = ""

        self.p_udp_source_port = ""
        self.p_udp_dest_port = ""
        self.p_udp_length = ""
        self.p_udp_checksum = ""

        self.p_icmp_type = ""
        self.p_icmp_code = ""
        self.p_icmp_checksum = ""
        self.p_icmp_restOfHeader = ""

    def fnc_db_insert(self, packet_db):

        self.p_eth_protocol = packet_db[0]["eth_protocol"]
        self.p_eth_dest_addr = packet_db[0]["eth_dest_addr"]
        self.p_eth_source_addr = packet_db[0]["eth_source_addr"]

        self.p_ip_version = packet_db[1]["ip_version"]
        self.p_ip_header_length = packet_db[1]["ip_header_length"]
        self.p_ip_type_of_service = packet_db[1]["ip_type_of_service"]
        self.p_ip_total_length = packet_db[1]["ip_total_length"]
        self.p_ip_identification = packet_db[1]["ip_identification"]
        self.p_ip_flags = packet_db[1]["ip_flags"]
        self.p_ip_fragment_offset = packet_db[1]["ip_fragment_offset"]
        self.p_ip_time_to_live = packet_db[1]["ip_time_to_live"]
        self.p_ip_protocol = packet_db[1]["ip_protocol"]
        self.p_ip_header_checksum = packet_db[1]["ip_header_checksum"]
        self.p_ip_source_addr = packet_db[1]["ip_source_addr"]
        self.p_ip_dest_addr = packet_db[1]["ip_dest_addr"]

        self.p_tcp_source_port = packet_db[2]["tcp_source_port"]
        self.p_tcp_dest_port = packet_db[2]["tcp_dest_port"]
        self.p_tcp_sequence_number = packet_db[2]["tcp_sequence_number"]
        self.p_tcp_ack_number = packet_db[2]["tcp_ack_number"]
        self.p_tcp_data_offset = packet_db[2]["tcp_data_offset"]
        self.p_tcp_reserved = packet_db[2]["tcp_reserved"]
        self.p_tcp_flags = packet_db[2]["tcp_flags"]
        self.p_tcp_window_size = packet_db[2]["tcp_window_size"]
        self.p_tcp_checksum = packet_db[2]["tcp_checksum"]
        self.p_tcp_urgent_pointer = packet_db[2]["tcp_urgent_pointer"]

        self.p_udp_source_port = packet_db[3]["udp_source_port"]
        self.p_udp_dest_port = packet_db[3]["udp_dest_port"]
        self.p_udp_length = packet_db[3]["udp_length"]
        self.p_udp_checksum = packet_db[3]["udp_checksum"]

        self.p_icmp_type = packet_db[4]["icmp_type"]
        self.p_icmp_code = packet_db[4]["icmp_code"]
        self.p_icmp_checksum = packet_db[4]["icmp_checksum"]

        db_packet = self.db_conn.NetworkTrafficColl.insert_one(
        {
            "ethernet_": {
                "eth_protocol": self.p_eth_protocol,
                "eth_dest_addr": self.p_eth_dest_addr,
                "eth_source_addr": self.p_eth_source_addr
            },
            "ip_": {
                "ip_version": self.p_ip_version,
                "ip_header_length": self.p_ip_header_length,
                "ip_type_of_service": self.p_ip_type_of_service,
                "ip_total_length": self.p_ip_total_length,
                "ip_identification": self.p_ip_identification,
                "ip_flags": self.p_ip_flags,
                "ip_fragment_offset": self.p_ip_fragment_offset,
                "ip_time_to_live": self.p_ip_time_to_live,
                "ip_protocol": self.p_ip_protocol,
                "ip_header_checksum": self.p_ip_header_checksum,
                "ip_source_addr": self.p_ip_source_addr,
                "ip_dest_addr": self.p_ip_dest_addr
            },
            "tcp_": {
                "tcp_source_port" : self.p_tcp_source_port,
                "tcp_dest_port": self.p_tcp_dest_port,
                "tcp_sequence_number": self.p_tcp_sequence_number,
                "tcp_ack_number": self.p_tcp_ack_number,
                "tcp_data_offset": self.p_tcp_data_offset,
                "tcp_reserved": self.p_tcp_reserved,
                "tcp_flags": self.p_tcp_flags,
                "tcp_window_size": self.p_tcp_window_size,
                "tcp_checksum": self.p_tcp_checksum,
                "tcp_urgent_pointer": self.p_tcp_urgent_pointer
            },
            "udp_": {
                "udp_source_port": self.p_udp_source_port,
                "udp_dest_port": self.p_udp_dest_port,
                "udp_length": self.p_udp_length,
                "udp_checksum": self.p_udp_checksum
            },
            "icmp_": {
                "icmp_type": self.p_icmp_type,
                "icmp_code": self.p_icmp_code,
                "icmp_checksum": self.p_icmp_checksum
            }
        }
    )