from Cls_PacketParse import *
from DAL.Cls_PacketInsert_DAL import *
from DAL.Cls_TcpStateInsert_DAL import *
from Cls_IPReputation import *

def fnc_insertPacketFindConn(packet):
    _inh_PacketParse = Cls_PacketParse()
    _inh_DBConnection = Cls_PacketInsert_DAL()
    _inh_DBTcpState = Cls_TcpStateInsert_DAL()
    _inh_IpReputation = Cls_IPReputations()

    packet_db_insert = []
    eth_db = {
        "eth_dest_addr": "",
        "eth_source_addr": "",
        "eth_protocol": ""
    }
    ip_db = {
        "ip_version": "",
        "ip_header_length": "",
        "ip_type_of_service": "",
        "ip_total_length": "",
        "ip_identification": "",
        "ip_flags": "",
        "ip_fragment_offset": "",
        "ip_time_to_live": "",
        "ip_protocol": "",
        "ip_header_checksum": "",
        "ip_source_addr": "",
        "ip_dest_addr": ""
    }
    tcp_db = {
        "tcp_source_port": "",
        "tcp_dest_port": "",
        "tcp_sequence_number": "",
        "tcp_ack_number": "",
        "tcp_data_offset": "",
        "tcp_reserved": "",
        "tcp_flags": "",
        "tcp_window_size": "",
        "tcp_checksum": "",
        "tcp_urgent_pointer": ""
    }
    udp_db = {
        "udp_source_port": "",
        "udp_dest_port": "",
        "udp_length": "",
        "udp_checksum": ""
    }
    icmp_db = {
        "icmp_type": "",
        "icmp_code": "",
        "icmp_checksum": ""
    }

    eth_db =_inh_PacketParse.fnc_parse_ethHeader(packet)
    if eth_db != False:
        if _inh_PacketParse.eth_protocol == 8:
            ip_db = _inh_PacketParse.fnc_parse_ipHeader(packet)

            if _inh_PacketParse.ip_protocol == 6:
                tcp_db =_inh_PacketParse.fnc_parse_tcpHeader(packet)

                synState = _inh_PacketParse.fnc_insert_syn()
                if synState != False:
                    _inh_DBTcpState.fnc_db_insert(synState)
                    print synState
                    print 1000 * '-'
                else:
                    synAckState =_inh_PacketParse.fnc_insert_synAck()

                    if synAckState != False:
                        _inh_DBTcpState.fnc_db_insert(synAckState)
                        print synAckState
                        print 1000 * '-'
                    else:
                        ackState = _inh_PacketParse.fnc_insert_ack()

                        if ackState != False:
                            _inh_DBTcpState.fnc_db_insert( _inh_IpReputation.fnc_IPReuputation(ackState))
                            #_inh_Psutil.fnc_getConnectionInformation()

            elif _inh_PacketParse.ip_protocol == 17:
                udp_db = _inh_PacketParse.fnc_parse_udpHeader(packet)
                # print("UDP parse")

            elif _inh_PacketParse.ip_protocol == 1:
                icmp_db = _inh_PacketParse.fnc_parse_icmpHeader(packet)
                # print("ICMP parse")

        packet_db_insert = [eth_db,ip_db,tcp_db,udp_db,icmp_db]
        _inh_DBConnection.fnc_db_insert(packet_db_insert)

