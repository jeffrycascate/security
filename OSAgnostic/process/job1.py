# 1@@run@@5@@Job 1@@win@@*
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
# [Code][Methodo By Run][Interval][Job Name][OS Type][Target Machine] ###
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
    from datetime import datetime
    import json
    import requests 

    class locator(object):
        def __init__(self):
            self.latitude = ""
            self.longitude = ""
            self.Successfully = False

    class Trace(object):
        def __init__(self,):
            self.Items = []
            self.Message = ""
            self.Severity = "NotAssigned"
            self.Successfully = False
            self.URL = ""
            self.IP = ""
            self.JobId = 0 
        
        def ConvertToJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    
    def LocatoIP(Ip):
        item = locator()
        try:
            url = "http://api.ipstack.com/{0}?access_key=842a3f2afb39f85f84991e39c4033bf1".format(
                Ip)
            headers = requests.utils.default_headers()
            headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            ret = requests.get(url, headers=headers, verify=False)
            body = json.loads(ret.content)
            item.latitude = body['latitude']
            item.longitude = body['longitude']
            item.Successfully = True
        except Exception as e:
            item.Successfully = False
        return item

    result = Trace()
    result.CreateDate = datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S:%f')
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
            if proc.name() == "powershell.exe" or proc.name() == "cmd.exe" or proc.name() == "Calculator.exe":
                item = Trace()
                item.CreateDate = datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S:%f')
                item.URL = ""
                item.IP = ""
                item.Message = "Se detecto la ejecucion de un processo:'{0}' con el pid='{1}' .... pata de queso".format(
                    proc.name(),  proc.pid)

                if proc.name() == "powershell.exe":
                    item.Severity = "Critical"
                if proc.name() == "cmd.exe":
                    item.Severity = "Warning"
                if proc.name() == "Calculator.exe":
                    item.Severity = "Information"

                item.Successfully = True

                pid = proc.pid
                print("{2} - Se inicio el el processo {0} con del pid {1}".format(
                    proc.name(), str(proc.pid), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                for c in psutil.net_connections(kind='inet'):
                    if c.pid == pid:
                        item.IP = c.raddr[0]
                        if item.IP is not None:
                            loc = LocatoIP(item.IP)
                            if loc.Successfully:
                                item.URL = 'https://www.google.com/maps?q={0},{1}'.format(
                                    loc.latitude, loc.longitude)
                result.Items.append(item)
        result.Successfully = True
    except Exception as e:
        print("Ocurrio un error ", str(e))
        result.Successfully = False

    return result


# if __name__ == "__main__":
#     ddd = run()
#     varr = ddd
