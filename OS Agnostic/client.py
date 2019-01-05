import threading
import time
import os
import sys
import fnmatch
import psutil
import platform
import socket
import json
import requests
from datetime import datetime

# configuration services
delimiter = '#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#'
FolderNameProcess = "process"


        

class ProcessRun(object):
    def __init__(self):
        self.Body = ""
        self.Path = ""
        self.NameMethod = ""
        self.Interval = 0

class Host(object):
    Items = []
    def __init__(self):
        self.HostName = ""
        self.IPLocal = ""
        self.IPPublic = ""
        self.Items = []

class ThreadingExample(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """
    ProcessRun = object

    def __init__(self, ProcessRun):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = ProcessRun.Interval
        self.ProcessRun = ProcessRun

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something

            #print("Star command that " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            try:
                funcs = {}
                exec(self.ProcessRun.Body, {}, funcs)
                for name in funcs:
                    if name == self.ProcessRun.NameMethod:
                        dd = funcs[name]
                        varrr = dd()

            except Exception as e:
                print("Ocurrio un error al ejecutar el archivo ",
                      self.ProcessRun.Path, ", Original Exception: ", str(e))
                print("End command that " +
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            time.sleep(self.interval)


def ManagerPrecess():
    ProcessRuns = []
    listOfFiles = os.listdir(os.path.join(os.getcwd(), FolderNameProcess))
    pattern = "*.py"
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            print(entry)
            item = ProcessRun()
            filePath = os.path.join(
                os.getcwd(),FolderNameProcess,  entry)

            bodyRAW = open(filePath, "r").read()
            item.Body = bodyRAW.split(
                delimiter)[1]
            configurationRAW = bodyRAW.split(
                delimiter)[0].replace('#', '').split(';')
            item.NameMethod = configurationRAW[0]
            item.Interval = int(configurationRAW[1])


            item.Path = filePath
            ProcessRuns.append(item)
    return ProcessRuns

def ManagerThreadProcess(process):
    print('sdfa')

def IpPublic():
    url = 'http://api.ipstack.com/check?access_key=842a3f2afb39f85f84991e39c4033bf1&format=1'
    headers = requests.utils.default_headers()  
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    ret = requests.get(url, headers=headers, verify=False)
    body = json.loads(ret.content)
    return body['ip']

def ManagerHost():
    item = Host()
    item.HostName =  platform.uname()[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    item.IPLocal= s.getsockname()[0]
    s.close()
    item.IPPublic = IpPublic()
    return item

if __name__ == "__main__":
    print('Starting process')
    ItemHost = ManagerHost()
    process = ManagerPrecess()
    for item in process:
        example = ThreadingExample(item)
    time.sleep(5000)
    print('End process')