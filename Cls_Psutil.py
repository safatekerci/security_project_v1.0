from psutil import *
from DAL.Cls_PsutilInsert_DAL import *
import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
AF_INET6 = getattr(socket, 'AF_INET6', object())

class Cls_Psutil(object):
    def __init__(self):
        self._inh_Psutil = Cls_PsutilInsert_DAL()
        self.psUtil_dict     = {}
        self.processId       = ''
        self.localAdd        = ''
        self.localAddPort    = ''
        self.remoteAdd       = ''
        self.remoteAddport   = ''
        self.family          = ''
        self.type            = ''
        self.satatus         = ''
        self.fileDescriptor  = ''
        self.processName     = ''
        self.processExePath  = ''
        self.processWorkPath = ''
        self.protocol        = ''
        self.Error           = ''
        self.protoCol_Map    = {(AF_INET, SOCK_STREAM) : 'tcp',
                                (AF_INET6, SOCK_STREAM): 'tcp6',
                                (AF_INET, SOCK_DGRAM)  : 'udp',
                                (AF_INET6, SOCK_DGRAM) : 'udp6',}

    def fnc_getConnectionInformation(self):
        packet = net_connections('tcp')  # Get all connection on pc(like netstat)
        for data in packet:
            self.localAdd          = data.__getattribute__('laddr')[0]
            self.localAddPort      = data.__getattribute__('laddr')[1]
            if data.__getattribute__('raddr'):
                self.remoteAddress = data.__getattribute__('raddr')[0]
                self.remoteAddport = data.__getattribute__('raddr')[1]
                print self.remoteAddress
            else:
                self.remoteAddress = "Empty"
                self.remoteAddport = "Empty"
            self.satatus           = data.__getattribute__('status')
            self.protocol          = self.protoCol_Map[data.__getattribute__('family'),data.__getattribute__('type')]
            self.processId         = data.__getattribute__('pid')
            self.fnc_getProcosessInfo()

            self.psUtil_dict={
            "processID": self.processId,
            "localAdd": self.localAdd,
            "localAddPort": self.localAddPort,
            "remoteAdd": self.remoteAddress,
            "remoteAddport": self.remoteAddport,
            "protocol": self.protocol,
            "processName": self.processName,
            "processExePath": self.processExePath,
            "processWorkPath": self.processWorkPath,
            }
            self._inh_Psutil.fnc_db_insert(self.psUtil_dict)
    def fnc_getProcosessInfo(self):
        try:
            if pid_exists(self.processId):
                process             = Process(self.processId)
                self.processName    = process.name()
                self.processExePath = process.exe()
                self.processWorkPath = process.cwd()
        except AccessDenied:
            self.Error             = "Prosese erisime izin verilmiyor!"

'''
if __name__ == '__main__':
    denemeP = Cls_Psutil()
    denemeP.getConnectionInformation()
'''