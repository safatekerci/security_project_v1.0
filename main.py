from Cls_InsertPacketFindConn import *
import pcapy
import time
import threading
def main():
    cap = pcapy.open_live('\Device\NPF_{D30712A8-2060-49A9-A978-D8A919E264D8}', 65536, 1, 0)
    while True:
        time.sleep(0.2)
        (header, packet) = cap.next()
        t = threading.Thread(target=fnc_insertPacketFindConn , args=(packet,))
        t.start()

if __name__ == "__main__":
    main()
