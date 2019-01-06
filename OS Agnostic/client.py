# region Imports
import threading
import time
import os
import sys
import platform
import fnmatch
import psutil
import socket
import json
import requests
import pymssql
from pathlib import Path
from ftplib import FTP
from datetime import datetime
from getmac import get_mac_address
from ClientMySQL import *

# endregion

# region Configurations

# configuration services
delimiter = '#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#'
FolderNameProcess = "process"
FolderProcessPath = os.path.join(os.getcwd(), FolderNameProcess)
IsReset = False

#MySQl Configuration
MySQLHost = '186.177.106.36'
MySQLUser = 'root'
MySQLPassword = 'Jcv1821@t5'
MySQLDatabase = 'osagnostic'
  

#region FPT Configuration
FTPTIP = "192.168.0.14"
FTPUser =  "Test"
FTPPassword = "c12345"
FTPPath = '/Configuration'
#endregion

# endregion

# region Class DTOS


class OS(object):
    def __init__(self):
        self.Name = ""
        self.System = ""
        self.Release = ""
        self.Architecture = ""

class Job(object):
    def __init__(self):
        self.Body = ""
        self.Path = ""
        self.NameMethod = ""
        self.Interval = 0

class Host(object):
    Jobs = []
    OS = OS()

    def __init__(self):
        self.Name = ""
        self.IPLocal = ""
        self.IPPublic = ""
        self.MacAddress = ""
        self.Jobs = []
        self.OS = OS()

class ManagerThreadJob(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """
    Job = object

    def __init__(self, Job):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = Job.Interval
        self.Job = Job

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something

            # print("Star command that " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            try:
                funcs = {}
                exec(self.Job.Body, {}, funcs)
                for name in funcs:
                    if name == self.Job.NameMethod:
                        bodyFuntion = funcs[name]
                        callResult = bodyFuntion()

            except Exception as e:
                print("Ocurrio un error al ejecutar el archivo ",
                      self.Job.Path, ", Original Exception: ", str(e))
                print("End command that " +
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            time.sleep(self.interval)

class ManagerThreadJob1(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """
    Job = object

    def __init__(self, Job):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = Job.Interval
        self.Job = Job

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something

            # print("Star command that " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            try:
                funcs = {}
                exec(self.Job.Body, {}, funcs)
                for name in funcs:
                    if name == self.Job.NameMethod:
                        bodyFuntion = funcs[name]
                        callResult = bodyFuntion()

            except Exception as e:
                print("Ocurrio un error al ejecutar el archivo ",
                      self.Job.Path, ", Original Exception: ", str(e))
                print("End command that " +
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            time.sleep(self.interval)

# endregion

# region Methods


def ManagerPrecess():
    Jobs = []
    listOfFiles = os.listdir(FolderProcessPath)
    pattern = "*.py"
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            print(entry)
            item = Job()
            filePath = os.path.join(FolderProcessPath,  entry)

            bodyRAW = open(filePath, "r").read()
            item.Body = bodyRAW.split(
                delimiter)[1]
            configurationRAW = bodyRAW.split(
                delimiter)[0].replace('#', '').split(';')
            item.NameMethod = configurationRAW[0]
            item.Interval = int(configurationRAW[1])

            item.Path = filePath
            Jobs.append(item)
    return Jobs


def ManagerThreadProcess(process):
    print('')


def IpPublic():
    result = "127.0.0.1"
    try:
        url = 'http://api.ipstack.com/check?access_key=842a3f2afb39f85f84991e39c4033bf1&format=1'
        headers = requests.utils.default_headers()
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        ret = requests.get(url, headers=headers, verify=False)
        body = json.loads(ret.content)
        result = body['ip']
    except Exception as e:
        print("Ocurrio un error al tratar de extrar la ip local ",
              ", Original Exception: ", str(e))
    return result


def IpLocal():
    result = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        result = s.getsockname()[0]
        s.close()
    except Exception as e:
        print("Ocurrio un error al tratar de extrar la ip local ",
              ", Original Exception: ", str(e))
    return result


def MacAddress(ip):
    result = ""
    try:
        result = get_mac_address(ip=ip)
    except Exception as e:
        print("Ocurrio un error al tratar de extrar la MacAddres ",
              ", Original Exception: ", str(e))
    return result


def ManagerOS():
    item = OS()
    item.Name = os.name
    item.System = platform.system()
    item.Release = platform.release()
    item.Architecture = platform.architecture()[0]
    return item


def ManagerHost():
    item = Host()
    item.Name = platform.uname()[1]
    item.IPLocal = IpLocal()
    item.IPPublic = IpPublic()
    item.MacAddress = MacAddress(item.IPLocal)
    # OS
    item.OS = ManagerOS()
    item.Jobs = ManagerPrecess()
    return item


def ManagerFTPCheckUpdates():
    result = False
    try:
        ftp = FTP(FTPTIP)
        ftp.login(FTPUser, FTPPassword)
        ftp.cwd(FTPPath)
        ftp.retrlines('LIST')
        filenames = []
        ftp.retrlines('NLST', filenames.append)
        for filename in filenames:
            datetimeftp = ftp.sendcmd('MDTM ' + filename)
            pathFile = os.path.join(FolderProcessPath, filename)
            my_file = Path(pathFile)
            if my_file.is_file():
                datetimepc = os.path.getmtime(
                    os.path.join(FolderProcessPath, filename))
                modifiedTimeFtp = datetime.strptime(
                    datetimeftp[4:], "%Y%m%d%H%M%S").strftime("%d %b %Y %H:%M:%S")
                modifiedTimePc = datetime.fromtimestamp(
                    datetimepc).strftime("%d %b %Y %H:%M:%S")
                if modifiedTimeFtp > modifiedTimePc:
                    with open( pathFile, 'wb' ) as file :
                        ftp.retrbinary('RETR %s' % filename, file.write)
                    result = True
            else:
                with open( pathFile, 'wb' ) as file :
                    ftp.retrbinary('RETR %s' % filename, file.write)
                result = True
        ftp.quit()
    except Exception as e:
        print("Ocurrio un error al tratar de extrar la ip local ",
              ", Original Exception: ", str(e))
    return result

def  ExistInServer(Host):
    db = CreateInstance(Host= MySQLHost, User= MySQLUser, Password= MySQLPassword, Database= MySQLDatabase)
    query = "select ID from host where Name = '{0}'".format(Host.Name)
    parameters = ()
    ExisteInServer = ExecuteCommand(db, query, parameters)
    db.close()
    return ExisteInServer

def  CreateHost(Host):
    db = CreateInstance(Host= MySQLHost, User= MySQLUser, Password= MySQLPassword, Database= MySQLDatabase)
    query = "INSERT INTO host( Name, IPLocal, IPPublic, MacAddress, State) " \
                 " VALUES ('{0}', '{1}','{2}', '{3}', {4});".format(Host.Name, Host.IPLocal, Host.IPPublic, Host.MacAddress, 1)
    parameters = ()
    ExisteInServer = ExecuteCommand(db, query, parameters)
    db.close()
    return ExisteInServer

def ManagerHostDataAccess(Host):
    ExisteInServer = ExistInServer(Host)
    if ExisteInServer.Successfully:
       if ExisteInServer.RowCount == 0:
           result = CreateHost(Host)
       else:
           print('dd')
    db.close()

# endregion


if __name__ == "__main__":
    ManagerFTPCheckUpdates()
    print('Starting process')
    ItemHost = ManagerHost()
    ManagerHostDataAccess(ItemHost)
    process = ManagerPrecess()
    for item in process:
        example = ManagerThreadJob(item)
    time.sleep(5000)
    print('End process')
