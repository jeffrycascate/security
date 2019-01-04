import os
import sys
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


def run():
    IsWork = False

    try:
        #IPsLocations = []
        IsWork = True
        procs = list(psutil.process_iter())
        #procs = sorted(procs, key=lambda proc: proc.name())
        #proc_names = {}
        # for p in psutil.process_iter(attrs=['pid', 'name']):
        #    proc_names[p.info['pid']] = p.info['name']

        # for proc in procs:
        #    if proc.name() == "powershell.exe":
        #        pid = proc.pid
        #        for c in psutil.net_connections(kind='inet'):
        #            if c.pid == pid:
        #                print(c)

        #print("Finished log update!")
        #print("writing new log data!")

        print("Called run")
        IsWork = True
    except:
        #e = sys.exc_info()
        #print("Ocurrio un error", e)
        IsWork = False

    return IsWork


def run1():
    IsWork = False
    try:
        IPsLocations = []

        separator = "-" * 80
        format = "%7s %7s %12s %12s %30s, %s"
        format2 = "%7.4f %7.2f %12s %12s %30s, %s"

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
        print("writing new log data!")

        print("Result " + str(True))
        IsWork = True
    except:
        e = sys.exc_info()[0]
        print("Ocurrio un error")
        IsWork = False

    return IsWork


if __name__ == "__main__":
    ddd = run()
