#1@@run@@5@@Job 1@@*@@None
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
# dasdfas Hola
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
    from datetime import datetime

    IsWork = False
    try:
        #IPsLocations = []
        procs = list(psutil.process_iter())
        procs = sorted(procs, key=lambda proc: proc.name())
        proc_names = {}
        for p in psutil.process_iter(attrs=['pid', 'name']):
            proc_names[p.info['pid']] = p.info['name']

        for proc in procs:
            if proc.name() == "powershell.exe" or proc.name() == "cmd.exe":
                pid = proc.pid
                print("{2} - Se inicio el el processo {0} con del pid {1}".format(
                    proc.name(), str(proc.pid), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                for c in psutil.net_connections(kind='inet'):
                    if c.pid == pid:
                        print(str(c))

        print("Finished log update!")
        print("writing new log data!")

        print("Called run")
        IsWork = True
    except Exception as e:
        print("Ocurrio un error ", str(e))
        IsWork = False

    return IsWork


# if __name__ == "__main__":
#    ddd = run()
