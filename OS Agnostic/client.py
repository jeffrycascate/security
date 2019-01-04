import os
import psutil
import time


class Process(object):
    def __init__(self):
        self.Protocolo = 0
        self.RemoteAddress = ""
        self.Status = ""
        self.PID = ""
        self.ProgramName = ""
        self.As = ""
        self.City = ""
        self.Country = ""
        self.CountryCode = ""
        self.ISP = ""
        self.Latitud = ""
        self.Longitud = ""
        self.Organization = ""
        self.Region = ""
        self.RegionName = ""
        self.ZIP = ""


IPsLocations = []

logPath = os.path.join(os.getcwd())
if not os.path.exists(logPath):
    os.mkdir(logPath)

separator = "-" * 80
format = "%7s %7s %12s %12s %30s, %s"
format2 = "%7.4f %7.2f %12s %12s %30s, %s"
while 1:
    procs = list(psutil.process_iter())
    procs = sorted(procs, key=lambda proc: proc.name())
    proc_names = {}
    for p in psutil.process_iter(attrs=['pid', 'name']):
        proc_names[p.info['pid']] = p.info['name']

    for proc in procs:
        if proc.name() == "powershell.exe":
            pid = proc.pid
            for c in psutil.net_connections(kind='inet'):
                if c.pid == pid:
                    dd = c

    print("Finished log update!")
    time.sleep(300)
    print("writing new log data!")
