from pymongo import MongoClient

class Cls_TcpStateInsert_DAL(object):

    def __init__(self):
        self.client = MongoClient()
        self.db_conn = self.client.ConnectionSecurityDB

    def fnc_db_insert(self,packet_db):

        if packet_db["packet_type"] == "syn":
            self.db_conn.TcpConnColl.insert_one(
            {
                "id"                       : packet_db["id"],
                "ip_source_addr"           : packet_db["ip_source_addr"],
                "ip_dest_addr"             : packet_db["ip_dest_addr"],
                "synPacket_sequence_num"   : packet_db["synPacket_sequence_num"],
                "synAckPacket_sequence_num": packet_db["synAckPacket_sequence_num"],
                "ackPacket_ack_num"        : packet_db["ackPacket_ack_num"],
                "tcp_state"                : packet_db["tcp_state"],
                "host_name"                : packet_db["host_name"],
                "ip_reputation"            : packet_db["ip_reputation"],
                "dns_name"                 : packet_db["dns_name"],

            })

        elif packet_db["packet_type"] == "synAck":
            self.db_conn.TcpConnColl.update(
            {    "ip_source_addr"        : packet_db["ip_source_addr"],
                 "ip_dest_addr"          : packet_db["ip_dest_addr"],
                 "synPacket_sequence_num":int(packet_db["synPacket_sequence_num"])
            },
            {
                "$set": {"synAckPacket_sequence_num": packet_db["synAckPacket_sequence_num"]}
            })

        elif packet_db["packet_type"] == "ack":
            self.db_conn.TcpConnColl.update(
            {
                "ip_source_addr": packet_db["ip_source_addr"],
                "ip_dest_addr": packet_db["ip_dest_addr"],
                "synAckPacket_sequence_num": int(packet_db["synAckPacket_sequence_num"])
            },
            {
                "$set": {
                            "ackPacket_ack_num": packet_db["ackPacket_ack_num"],
                            "tcp_state":packet_db["tcp_state"],
                            "host_name":packet_db["host_name"],
                            "dns_name": packet_db["dns_name"],
                            "ip_reputation":packet_db["ip_reputation"]
                        }
            })

