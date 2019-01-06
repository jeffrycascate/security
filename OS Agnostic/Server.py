#region Imports
import threading
import time
import os
from datetime import datetime
#endregion

if __name__ == "__main__":
    IsRun = True
    while IsRun:
        filePath = os.path.join(os.getcwd(), "Server.config")
        bodyRAW = open(filePath, "r").read()
        if bodyRAW == '0':
            IsRun = False
            print("Stop services that " +
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(20)
        print("Executed to" +
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("Exit program to " +
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
