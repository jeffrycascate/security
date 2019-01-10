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
from ClientMySQL import *


# endregion


def ManagerJobCreate(Host, Job):
    db = CreateInstance(Host=MySQLHost, User=MySQLUser,
                        Password=MySQLPassword, Database=MySQLDatabase)
    query = "Insert Into Job( `Code`, `Name`, `Interval`, `HostId`, `OSType`, `CreateDate`, `UpdateDate` ) " \
        " VALUES( '{0}','{1}',   {2},    {3},  '{4}' , SYSDATE(), SYSDATE());".format(
            Job.Code, Job.Name, Job.Interval,  Host.Id, Job.OSType)
    parameters = ()
    result = ExecuteCommand(db, query, parameters)
    if result.Successfully:
        Job.Id = result.LastRowId
    db.close()
