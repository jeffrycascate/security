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
from dateutil.parser import *
from pathlib import Path
from ftplib import FTP
from datetime import datetime
from getmac import get_mac_address
import jsonpickle

# endregion

# region Configurations

# General
BLUE = '34m'
delimiter = '#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#'
FolderNameProcess = "process"
FolderProcessPath = os.path.join(os.getcwd(), FolderNameProcess)
filePathConfiguration = os.path.join(os.getcwd(), "Client.config")
IsReset = False
IsRun = True

URLServices = "http://186.177.106.143:5010/api/"

# region FPT Configuration
FTPTIP = "186.177.106.143"
FTPUser = "Test"
FTPPassword = "c12345"
FTPPath = '/Configuration'
# endregion

# endregion


# region Methods

def display_colored_text(color, text):
    colored_text = f"\033[{color}{text}\033[00m"
    return colored_text


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
                delimiter)[0].replace('#', '').split('@@')

            item.Code = int(configurationRAW[0])
            item.NameMethod = configurationRAW[1].rstrip()
            item.Interval = int(configurationRAW[2])
            item.Name = configurationRAW[3].rstrip()
            item.OSType = configurationRAW[4].rstrip()

            Targets = configurationRAW[5].rstrip()
            if Targets != '*':
                for itemTarget in Targets.split(';'):
                    item.Targets.append(itemTarget)
            else:
                item.Targets = []

            item.Path = filePath
            Jobs.append(item)
    return Jobs


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
    result = ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        result = s.getsockname()[0]
        s.close()
    except Exception as e:
        print("Ocurrio un error al tratar de extrar la ip local ",
              ", Original Exception: ", str(e))
    if result == "":
        try:
            result = socket.gethostbyname(socket.gethostname())
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
    item.Name = platform.uname()[1].rstrip()
    item.IPLocal = IpLocal()
    item.IPPublic = IpPublic()
    item.MacAddress = MacAddress(item.IPLocal)
    # OS
    item.OS = ManagerOS()

    TemporalJobs = ManagerPrecess()
    for itemJob in TemporalJobs:
        AllowSO = False
        AllowTarget = False

        # Check if job is that allowed by host for type system operation
        if itemJob.OSType == '*':
            AllowSO = True
        else:
            if itemJob.OSType.lower() in item.OS.System.lower():
                AllowSO = True

        # Check if job is that allowed by name host
        if len(itemJob.Targets) == 0:
            AllowTarget = True
        else:
            for itemTarger in itemJob.Targets:
                if itemTarger.lower() == item.Name.lower():
                    AllowTarget = True
        if AllowSO and AllowTarget:
            item.Jobs .append(itemJob)

    return item


def ManagerFTPCheckUpdates(IsFirts):
    result = False
    ftp = ""

    try:
        ftp = FTP(FTPTIP)
        ftp.login(FTPUser, FTPPassword)
        ftp.set_pasv(False)
        ftp.cwd(FTPPath)
        ftp.retrlines('LIST')
        filenames = []
        ftp.retrlines('NLST', filenames.append)

        lines = []
        ftp.dir(FTPPath, lines.append)

        for line in lines:
            tokens = line.split(maxsplit=9)
            filename = tokens[8]
            pathFile = os.path.join(FolderProcessPath, filename)
            if IsFirts == False:
                time_str = tokens[5] + " " + tokens[6] + " " + tokens[7]
                modifiedTimeFtp = parse(time_str)

                my_file = Path(pathFile)
                if my_file.is_file():
                    datetimepc = os.path.getmtime(
                        os.path.join(FolderProcessPath, filename))
                    datetimepc = datetime.fromtimestamp(datetimepc)
                    if modifiedTimeFtp > datetimepc:
                        with open(pathFile, 'wb') as file:
                            ftp.retrbinary('RETR %s' % filename, file.write)
                        result = True
                else:
                    with open(pathFile, 'wb') as file:
                        ftp.retrbinary('RETR %s' % filename, file.write)
                    result = True
            else:
                with open(pathFile, 'wb') as file:
                    ftp.retrbinary('RETR %s' % filename, file.write)
                result = True
        ftp.quit()
    except Exception as e:
        print("Error ManagerFTPCheckUpdates ",
              ", Original Exception: ", str(e))
    return result


def ManagerJobsExistInServer(Host, Job):
    result = ""
    try:
        url = URLServices + \
            'Job/Exist?Code={}&HostId={}'.format(Job.Code, Host.Id)
        headers = requests.utils.default_headers()
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        ret = requests.get(url, headers=headers, verify=False)
        body = json.loads(ret.content)
        result = body
    except Exception as e:
        print("Ocurrio un error al tratar de extrar la ip local ",
              ", Original Exception: ", str(e))
    return result


def ManagerJobCreate(Host, Job):
    result = ""
    try:
        url = URLServices + 'Job/Add'
        headers = requests.utils.default_headers()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        Job.HostId = Host.Id
        ret = requests.post(url, Job.ConvertToJSON(),
                            headers=headers, verify=False)
        body = json.loads(ret.content)
        result = body
        Job.Id = body['Id']
    except Exception as e:
        print("Ocurrio un error al tratar de extrar la ip local ",
              ", Original Exception: ", str(e))
    return result


def ManagerHostDataAccess(Host):
    ExisteInServer = ManagerHostExistInServer(Host)
    if ExisteInServer['Exist'] == False:
        ManagerHostCreate(Host)
    else:
        Host.Id = int(ExisteInServer['Id'])
    ManagerJobsDataAccess(Host)


def ManagerHostCreate(Host):
    result = False
    try:
        url = URLServices + 'Host/Add'
        headers = requests.utils.default_headers()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        ret = requests.post(url, Host.ConvertToJSON(),
                            headers=headers, verify=False)
        body = json.loads(ret.content)
        result = body
        Host.Id = int(result['Id'])
    except Exception as e:
        print("Ocurrio un error al tratar de extrar la ip local ",
              ", Original Exception: ", str(e))
    return result


def ManagerHostExistInServer(Host):
    result = False
    try:
        url = URLServices + 'Host/Exist?Name=' + Host.Name
        headers = requests.utils.default_headers()
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        ret = requests.get(url, headers=headers, verify=False)
        body = json.loads(ret.content)
        result = body
    except Exception as e:
        print("Ocurrio un error al tratar de extrar la ip local ",
              ", Original Exception: ", str(e))
    return result


def ManagerJobsDataAccess(Host):
    for item in Host.Jobs:
        item.HostId = Host.Id
        ExisteInServer = ManagerJobsExistInServer(Host, item)
        if ExisteInServer['Exist'] == False:
            ManagerJobCreate(Host, item)
        else:
            item.Id = int(ExisteInServer['Id'])
        


def ManagerTraceDataAccess(JobId, Trace):
    result = ""
    try:
        if Trace != None:
            url = URLServices + 'Trace/Add'
            headers = requests.utils.default_headers()
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            Trace.JobId = JobId
            
            ret = requests.post(url, json.dumps(vars(Trace), sort_keys=True, indent=4),
                                headers=headers, verify=False)
            body = json.loads(ret.content)
            result = body
    except Exception as e:
        print("Ocurrio un error ManagerTraceDataAccess, Original Exception: ", str(e))


def ManagerHostState(Host, State):
    result = False
    try:
        url = URLServices + 'Host/StateChange?Id={0}&State={1}'.format(Host.Id, State)
        headers = requests.utils.default_headers()
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        ret = requests.get(url, headers=headers, verify=False)
        body = json.loads(ret.content)
        result = body
    except Exception as e:
        print("Ocurrio un error al tratar de extrar la ip local ",
              ", Original Exception: ", str(e))
    return result

# endregion


# region Class DTOS


class OS(object):
    def __init__(self):
        self.Name = ""
        self.System = ""
        self.Release = ""
        self.Architecture = ""

    def ConvertToJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Job(object):
    def __init__(self):
        self.Id = 1
        self.Body = ""
        self.Path = ""
        self.NameMethod = ""
        self.Interval = 0
        self.Code = 0
        self.Name = ""
        self.OSType = ""
        self.Targets = []
        self.HostId = 0

    def ConvertToJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Host(object):

    def __init__(self):
        self.Id = 0
        self.Name = ""
        self.IPLocal = ""
        self.IPPublic = ""
        self.MacAddress = ""
        self.Jobs = []
        self.OS = OS()

    def ConvertToJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Trace(object):

    def __init__(self):
        self.Id = 0
        self.Message = ""
        self.Severity = "NotAssigned"
        self.Successfully = False
        self.URL = ""
        self.IP = ""
        self.JobId = 0 

    def ConvertToJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


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


class ManagerThreadHostLive(Host):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """
    Host = Host

    def __init__(self, Host):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = 5
        self.Host = Host

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:

            try:
                result = ManagerHostState(self.Host, True)
                if result == True:
                    print(
                        "A signal is sent to the active server for the host '{0}', to: {1}".format(self.Host.Name,  datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            except Exception as e:
                print("Ocurrio un error al Update live, Original Exception: ", str(e))

            time.sleep(self.interval)


class ManagerThreadByJob(Host, Job):

    Host = Host
    Job = Job

    def __init__(self, Host, Job):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = Job.Interval
        self.Host = Host
        self.Job = Job
        self.IsRun = True

        self.thread = threading.Thread(target=self.run,  args=(
        ), name="Name={0}, Interval={1}".format(Job.Name, Job.Interval))
        self.thread.daemon = True
        self.shutdown_flag = threading.Event()
        self.thread.start()

    def run(self):
        """ Esta seccion es solo la primera vez que se hace para que queden activos lo thread de pocessos """
        while self.IsRun:
            try:
                print("Se llama el proceso {0} cada {1}".format(
                    self.Job.Name, self.Job.Interval))

                funcs = {}
                exec(self.Job.Body, {}, funcs)
                for name in funcs:
                    if name == self.Job.NameMethod:
                        bodyFuntion = funcs[name]
                        callResult = bodyFuntion()
                        if callResult.Successfully:
                            print(
                                "Ejecucion del modulo {0}".format(self.Job.Name))
                            for item in callResult.Items:
                                ManagerTraceDataAccess(self.Job.Id, item)
                        else:
                            print(
                                "Fallo la ejecucion del modulo {0}".format(self.Job.Name))

            except Exception as e:
                print("Ocurrio un error al Update live, Original Exception: ", str(e))

            time.sleep(self.interval)
        print("Jobs '{0}' is being stopped".format(self.Job.Name))
        self.shutdown_flag.set()


def ThreadsMake(Host):
    result = []
    for item in Host.Jobs:
        ItemThread = ManagerThreadByJob(Host, item)
        result.append(ItemThread)
    return result


def ThreadsStop(Pools):
    for item in Pools:
        item.IsRun = False


class ManagerThreads(Host):

    Host = Host

    def __init__(self, Host):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = 5
        self.Host = Host

        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True                           # Daemonize thread
        self.thread.start()                                 # Start the execution

    def run(self):
        """ Esta seccion es solo la primera vez que se hace para que queden activos lo thread de pocessos """
        Pools = ThreadsMake(self.Host)

        while True:
            try:
                if ManagerFTPCheckUpdates(False):
                    print(
                        "**************************************************************************")
                    print("Reiniciar manager thread - {0}".format(
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    print(
                        "**************************************************************************")

                    self.Host = ManagerHost()
                    ThreadsStop(Pools)
                    ManagerHostDataAccess(self.Host)
                    Pools = ThreadsMake(self.Host)

                else:
                    print(
                        "**************************************************************************")
                    print("Sin Reiniciar manager thread - {0}".format(
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    print(
                        "**************************************************************************")

            except Exception as e:
                print("Ocurrio un error ManagerThreads, Original Exception: ", str(e))

            time.sleep(self.interval)


# endregion


if __name__ == "__main__":
    print('Starting process')

    if 'CCSERVER' == platform.uname()[1]:
        FTPTIP = "192.168.0.14"
        MySQLHost = "192.168.0.14"
        URLServices = "http://localhost:5006/api/"
        

    ManagerFTPCheckUpdates(True)

    ItemHost = ManagerHost()

    ManagerHostDataAccess(ItemHost)

    ManagerThreadHostLive(ItemHost)

    ManagerThreads(ItemHost)

    bodyRAW = open(filePathConfiguration, "r").read()

    if bodyRAW == '0':
        IsRun = False

    while IsRun:
        bodyRAW = open(filePathConfiguration, "r").read()
        if bodyRAW == '0':
            IsRun = False
            print("Stop services client that " +
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            print("Executed - Update Hosts " +
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(30)
        print("Executed to client" +
              datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("Exit program to client" +
          datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
