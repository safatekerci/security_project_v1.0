from _winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, OpenKey, QueryValueEx
from netifaces import interfaces, ifaddresses, AF_INET
import netifaces
import sys

class Cls_Interface(object):

    def __init__(self):
        lst_myDevices = []

    def fnc_get_myDevices(self):
        '''try:
            myDevices = pcapy.findalldevs()
            print "Makinedeki interfaceler ;"

            i = 1
            for d in myDevices:
                print "%s).  %s" % (i, QueryValueEx(d, 'Name')[0])

                i += 1
            return myDevices
        except:
            print "Interfaceler listelenirken hata olustu."
            sys.exit()
        '''
        try:
            try:
                lst_myDevices = netifaces.interfaces()
            except Exception as ex:
                print "Interfaceler listelenirken hata olustu. >> %s", ex.message
                sys.exit()

            try:
                iface_names = ['(unknown)' for i in range(len(lst_myDevices))]
                reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
                reg_key = OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')

                for i in range(len(lst_myDevices)):
                    try:
                        reg_subkey = OpenKey(reg_key, lst_myDevices[i] + r'\Connection')
                        print "\\Device\\NPF_" + lst_myDevices[i] + " = " + QueryValueEx(reg_subkey, 'Name')[0]
                    except Exception as ex:
                        pass

            except Exception as ex:
                print "Interfacelere isim verilirken hata olustu. >> %s", ex.message

            for i, dev in enumerate(lst_myDevices):
                lst_myDevices[i] = "\\Device\\NPF_" + dev


            return  lst_myDevices

        except Exception as ex:
            print "Interfaceler listelenirken hata olustu.>> %s", ex.message
            sys.exit()

        def fnc_get_myIPv4(self):
            myInterface = '\Device\NPF_{C4AD2A8D-8326-4992-A10B-FFC055E280F6}'
            myInterface = myInterface.replace('\Device\NPF_', '')
            myIp = [i['addr'] for i in ifaddresses(myInterface).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
            myIp = str(myIp).replace('u', '').replace('[', '').replace(']', '').replace('\\', '')
            return myIp[1:12]
