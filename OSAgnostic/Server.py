#region Imports
import threading
import time
import os
from datetime import datetime
from ClientMySQL import *
#endregion

#region Configuration
filePathConfiguration = os.path.join(os.getcwd(), "Server.config")
interval = 30

#MySQl Configuration
MySQLHost = 'localhost'
MySQLUser = 'root'
MySQLPassword = 'Jcv1821@t5'
MySQLDatabase = 'osagnostic'

#endregion

#region Methods
def  UpdateHosts():
    db = CreateInstance(Host= MySQLHost, User= MySQLUser, Password= MySQLPassword, Database= MySQLDatabase)
    query = "update host set State = b'0' where ADDTIME(updatedate , '0:00:10') <  SYSDATE();"
    parameters = ()
    ExisteInServer = ExecuteCommand(db, query, parameters)
    db.close()
    return ExisteInServer
#endregion

if __name__ == "__main__":
    IsRun = True
    bodyRAW = open(filePathConfiguration, "r").read()
    
    if bodyRAW == '0':
        IsRun = False

    while IsRun:
        bodyRAW = open(filePathConfiguration, "r").read()
        if bodyRAW == '0':
            IsRun = False
            print("Stop services that " +
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            result = UpdateHosts()
            print("Executed - Update Hosts " +
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(interval)
        print("Executed to " +
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("Exit program to " +
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
