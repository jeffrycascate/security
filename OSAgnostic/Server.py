#region Imports
import threading
import time
import os
from datetime import datetime
import requests
import json
#endregion

#region Configuration
filePathConfiguration = os.path.join(os.getcwd(), "Server.config")
URLServices = "http://localhost:5006/api/"
interval = 30

#MySQl Configuration
MySQLHost = 'localhost'
MySQLUser = 'root'
MySQLPassword = 'Jcv1821@t5'
MySQLDatabase = 'osagnostic'

#endregion

#region Methods
def  UpdateHosts():
    result = False
    try:
        url = URLServices + 'Host/StateChangeServer'
        headers = requests.utils.default_headers()
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        ret = requests.get(url, headers=headers, verify=False)
        body = json.loads(ret.content)
        result = body
    except Exception as e:
        print("Ocurrio un error al tratar de extrar la ip local ",
              ", Original Exception: ", str(e))
    return result

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
