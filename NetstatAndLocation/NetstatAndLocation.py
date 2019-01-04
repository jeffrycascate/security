# paquete requeridos
#  psutil

import os
import platform
import socket
import psutil
import json
import requests
import pprint
import re

from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM

template = ' <!DOCTYPE html> \n'  \
    ' <html lang="en"> \n' \
    ' <head> \n' \
    ' <meta charset="utf-8">\n' \
    ' <meta http-equiv="X-UA-Compatible" content="IE=edge"> \n' \
    ' <meta name="viewport" content="width=device-width, initial-scale=1"> \n' \
    ' <title>Example of Bootstrap 3 Accordion</title> \n' \
    ' <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"> \n' \
    ' <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script> \n' \
    ' <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script> \n' \
    ' <script type="text/javascript"> \n' \
    ' {1} \n' \
    ' </script> \n' \
    ' </head> \n' \
    ' <body> \n' \
    ' <nav class="navbar navbar-inverse"> \n' \
    '   <div class="container-fluid"> \n' \
    '     <div class="navbar-header"> \n' \
    '       <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar"> \n' \
    '         <span class="icon-bar"></span> \n' \
    '         <span class="icon-bar"></span> \n' \
    '         <span class="icon-bar"></span>                        \n' \
    '       </button> \n' \
    '       <a class="navbar-brand" href="#">Connection my host analysis</a> \n' \
    '     </div> \n' \
    '   </div> \n' \
    ' </nav> \n' \
    ' <div class="bs-example"> \n' \
    '     <div class="panel-group" id="accordion">                \n' \
    '         {0} \n' \
    '     </div> \n' \
    ' </div> \n' \
    ' <script async defer src="http://maps.google.com/maps/api/js?key=AIzaSyCvDN-LuS_9_VFkR71Sc56P6y4cwWKvEpU&callback=drawMap"></script> \n' \
    ' </body> \n' \
    ' </html> \n'

itemTemplate = ' <div class="panel panel-default"> \n' \
    ' 	<div class="panel-heading"> \n' \
    ' 		<h4 class="panel-title"> \n' \
    ' 			<a data-toggle="collapse" data-parent="#accordion" href="#collapse{0}">{1}</a> \n' \
    ' 		</h4> \n' \
    ' 	</div> \n' \
    ' 	<div id="collapse{0}" class="panel-collapse collapse"> \n' \
    ' 		<div class="panel-body"> \n' \
    ' 		  <div class="row"> \n' \
    ' 			{2} \n' \
    ' 		  </div> \n' \
    ' 		</div> \n' \
    ' 	</div> \n' \
    ' </div> \n' \

elementTempalte = ' 					  <div class="col-sm-4">{0}</div> \n' \
                  ' 					  <div class="col-sm-8">{1}</div> \n' \

elementMapTempalte = ' 					  <div class="col-sm-4">{0}</div> \n' \
                     ' 					  <div id="map{1}" style="height: 250px;" class="col-sm-8"></div> \n' \

varMaps = 'map{0}'

elemnentInitMapTemplate = '        var map{0}Options = {1} zoom: 13, mapTypeId: google.maps.MapTypeId.ROADMAP, mapTypeControl: true, fullscreenControl: true {2} \n ' \
    '		map{0}Options.center = new google.maps.LatLng({3}, {4}); \n ' \
    '		map{0} = new google.maps.Map(document.getElementById("map{0}"), map{0}Options); \n ' \
    '		var marker{0} = new google.maps.Marker({1} position: new google.maps.LatLng({3}, {4}), map: map{0}, title: "{5}" {2}); \n ' \
    '		marker{0}.setMap(map{0}); \n ' \



class IPLocator(object):
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


def isNotEmpty(s):
    return bool(s and s.strip())


def LocationByIp(IP, Protocolo, Status, PID, ProgramName):
    if isNotEmpty(IP) and IP.find('127.0.0.1') == -1 and IP.find('localhost') == -1:
        try:
            if IP.find(":") != -1:
                IP = IP.split(":")[0]
            url = 'http://ip-api.com/json/' + IP
            pprint.pprint("Analyzing to " + IP)
            headers = requests.utils.default_headers()
            headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            ret = requests.get(url, headers=headers, verify=False)
            body = json.loads(ret.content)
            item = IPLocator()
            item.Protocolo = Protocolo
            item.RemoteAddress = IP
            item.Status = Status
            item.PID = PID
            item.ProgramName = ProgramName
            item.As = body['as']
            item.City = body['city']
            item.Country = body['country']
            item.CountryCode = body['countryCode']
            item.ISP = body['isp']
            item.Latitud = body['lat']
            item.Longitud = body['lon']
            item.Organization = body["org"]
            item.Region = body["region"]
            item.RegionName = body["regionName"]
            item.ZIP = body["zip"]
            IPsLocations.append(item)
        except requests.exceptions.RequestException as e:
            pprint.pprint(e)
        except:
            pprint.pprint("The ip could not be analyzed '" + IP + "'")


NameOS = platform.system()
# if NameOS.lower() == "windows":
# 1. correct el commando en el carpeta "python -m pip install -upgrade pip" esto para actulizar
# 2. Si deseas intalr paquetes debe ser en python-scripts "pip install psutil"

AD = "-"
AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM): 'udp',
    (AF_INET6, SOCK_DGRAM): 'udp6',
}
templ = "%-5s %-30s %-30s %-13s %-6s %s"
# print(templ % (
#    "Proto", "Local address", "Remote address", "Status", "PID",
#    "Program name"))
print("Start Analyzing")
proc_names = {}
for p in psutil.process_iter(attrs=['pid', 'name']):
    proc_names[p.info['pid']] = p.info['name']
for c in psutil.net_connections(kind='inet'):
    laddr = "%s:%s" % (c.laddr)
    raddr = ""
    NameProgram = proc_names.get(c.pid, '?')[:15]
    pro = proto_map[(c.family, c.type)]
    if c.raddr:
        raddr = "%s:%s" % (c.raddr)

    # print(templ % (
    #    pro,
    #    laddr,
    #    raddr or AD,
    #    c.status,
    #    c.pid or AD,
    #    NameProgram,
    # ))

    LocationByIp(raddr, pro,  c.status, c.pid, NameProgram)

if IPsLocations.count != 0:
    script_dir = os.path.dirname(__file__)
    rel_path = "report.html"
    abs_file_path = os.path.join(script_dir, rel_path)
    folder = os.path.join(os.path.expanduser('~'), "NABOO")
    if os.path.exists(folder) != True :
        os.mkdir(folder)
    abs_file_path = os.path.join(folder,rel_path)
    f = open(abs_file_path, 'w')
    body = ""
    index = 1
    bodyJS = "   var "
    for member in IPsLocations:
        items = ""
        items = items + elementTempalte.format("Protocolo", member.Protocolo)
        items = items + elementTempalte.format("IP", member.RemoteAddress)
        items = items + elementTempalte.format("Status", member.Status)
        items = items + elementTempalte.format("PID", member.PID)
        items = items + \
            elementTempalte.format("ProgramName", member.ProgramName)
        items = items + elementTempalte.format("As", member.As)
        items = items + elementTempalte.format("City", member.City)
        items = items + elementTempalte.format("Country", member.Country)
        items = items + \
            elementTempalte.format("Country Code", member.CountryCode)
        items = items + elementTempalte.format("ISP", member.ISP)
        items = items + elementTempalte.format("Latitud", member.Latitud)
        items = items + elementTempalte.format("Longitud", member.Longitud)
        items = items + elementTempalte.format("Region", member.Region)
        items = items + \
            elementTempalte.format("Region Name", member.RegionName)
        items = items + elementTempalte.format("ZIP", member.ZIP)
        items = items + \
            elementTempalte.format("Organization", member.Organization)

        items = items + \
            elementMapTempalte.format("Map", index)

        body = body + \
            itemTemplate.format(
                index, (member.RemoteAddress + '-' + member.As + '-' + member.Country), items)
        bodyJS = bodyJS + varMaps.format(index) + ' , '

        index = index + 1

    bodyJS = bodyJS[:-2] + ";\n"
    bodyJS = bodyJS + '\n'
    bodyJS = bodyJS + ' function drawMap() {\n'

    index = 1
    for member in IPsLocations:
        bodyJS = bodyJS + \
            elemnentInitMapTemplate.format(
                index, '{', '}', member.Latitud, member.Longitud, (member.As + ' ' + member.RemoteAddress))
        index = index + 1

    bodyJS = bodyJS + ' }\n'

    templateBody = template.format(body, bodyJS)
    f.writelines(templateBody)
    f.close()
    print("Path file:", abs_file_path)
print("I finish the analysis, please check a file called report.html")
# elif NameOS.lower() == "linux":

#print("SO:" + NameOS)
