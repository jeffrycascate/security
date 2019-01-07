#region Imports
import threading
import time
import os
from datetime import datetime
from ClientMySQL import *
#endregion

#region Configuration
filePath = os.path.join(os.getcwd(), "Server.config")

#MySQl Configuration
MySQLHost = '186.177.106.36'
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
    bodyRAW = open(filePath, "r").read()
    
    if bodyRAW == '0':
        IsRun = False

    while IsRun:
        bodyRAW = open(filePath, "r").read()
        if bodyRAW == '0':
            IsRun = False
            print("Stop services that " +
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            result = UpdateHosts()
            print("Executed - Update Hosts " +
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(10)
        print("Executed to " +
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("Exit program to " +
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
