# -*- coding: utf-8 -*-
# cmd yönetici olarak çalıştırılıp bulunan klasöre gelinmeldiir. >> python windowsService.py    şeklinde çalıştırılır.
# binaryPathName exe'nin olduğu path olarak değiştirilmelidir.

from pywinservicemanager.WindowsServiceConfigurationManager import CreateService
from pywinservicemanager.NewServiceDefinition import NewServiceDefinition
import pywinservicemanager.ConfigurationTypes as ConfigurationTypes


serviceName = 'BlackListService'
displayName = 'BlackListService'
binaryPathName = 'C:\\Users\\Safa\\Desktop\\BlackList\\dist\\Cls_BlackList.exe'  # değiştirilecek
startType = 'AUTO_START'
serviceType= 'WIN32_OWN_PROCESS'
errorControl= 'ERROR_IGNORE'
loadOrderGroup = None
dependencies= ['nsi']
description= 'BlackListService'
failureFlag = False
preShutdownInfo= 18000
serviceSIDInfo = 'SID_TYPE_UNRESTRICTED'
userName = None
password = None
delayedAutoStartInfo = True

failureActionList = []
delay = 1000
failureActionList.append(ConfigurationTypes.FailureActionTypeFactory.CreateRestartAction(delay))
failureActionList.append(ConfigurationTypes.FailureActionTypeFactory.CreateRunCommandAction(delay))
resetPeriod = 1
rebootMsg = 'MyRebootMessage'
commandLine = 'MyCommandLine'
#failureActions = FailureActionConfigurationType(failureActionList, resetPeriod, rebootMsg, commandLine)

newServiceDefinition = NewServiceDefinition(serviceName=serviceName,
                                            displayName=displayName,
                                            binaryPathName=binaryPathName,
                                            startType=startType,
                                            serviceType=serviceType,
                                            errorControl=errorControl,
                                            loadOrderGroup=loadOrderGroup,
                                            dependencies=dependencies,
                                            serviceStartName=userName,
                                            description=description,
                                            #failureActions=failureActions,
                                            failureFlag=failureFlag,
                                            preShutdownInfo=preShutdownInfo,
                                            serviceSIDInfo=serviceSIDInfo,
                                            delayedAutoStartInfo=delayedAutoStartInfo)

myService = CreateService(newServiceDefinition)
myService.Save(password)