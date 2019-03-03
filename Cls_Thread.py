import threading
from Cls_InsertPacketFindConn import *

class Cls_Thread (threading.Thread):
    def __init__(self, threadID, name,funcName):
        threading.Thread.__init__(self)
        self._inh_InsertPacketFindConn = Cls_InsertPacketFindConn()
        self.threadID = threadID
        self.name = name
        self.funcName = funcName

    def run(self):
        if self.funcName == "packetParse":
            print "Starting " + self.name
            self._inh_InsertPacketFindConn.fnc_insertPacketFindConn()
            print "Exiting " + self.name
        elif self.funcName == "psUtil":
            print "Starting " + self.name
            self._inh_psUtil.getConnectionInformation()
            print "Exiting " + self.name



