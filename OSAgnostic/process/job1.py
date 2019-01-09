# 1@@run@@5@@Job 1@@*@@None
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

from enum import Enum


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
    import psutil
    import os
    import sys
    import time
    from enum import Enum
    from datetime import datetime

    class Severity(Enum):
        NotAssigned = 0
        Information = 1
        Warning = 2
        Error = 3
        Critical = 4

    class Result(object):
        def __init__(self,):
            self.Items = []
            self.CreateDate = ""
            self.Message = ""
            self.Severity = Severity.NotAssigned
            self.Successfully = False
            self.URL = ""
            self.IP = ""

    result = Result()
    result.CreateDate = datetime.now()
    result.Message = "Processo de monitoreo de jobs"
    try:
        # IPsLocations = []
        # http://maps.google.com/maps?z=12&t=m&q=loc:38.9419+-78.3020 format
        procs = list(psutil.process_iter())
        procs = sorted(procs, key=lambda proc: proc.name())
        proc_names = {}
        for p in psutil.process_iter(attrs=['pid', 'name']):
            proc_names[p.info['pid']] = p.info['name']

        for proc in procs:
            if proc.name() == "powershell.exe" or proc.name() == "cmd.exe":
                item = Result()
                item.CreateDate = datetime.now()
                item.URL = ""
                item.IP = ""
                item.Message = "Se detecto la ejecucion de un processo:'{0}' con el pid='{1}'".format(
                    proc.name(),  proc.pid)

                item.Severity = Severity.Critical
                item.Successfully = True
                result.Items.append(item)

                pid = proc.pid
                print("{2} - Se inicio el el processo {0} con del pid {1}".format(
                    proc.name(), str(proc.pid), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                for c in psutil.net_connections(kind='inet'):
                    if c.pid == pid:
                        print(str(c))

        # print("Finished log update!")
        # print("writing new log data!")
        result.Successfully = True
    except Exception as e:
        print("Ocurrio un error ", str(e))
        result.Successfully = False

    return result


# if __name__ == "__main__":
#    ddd = run()
#    varr = ddd
