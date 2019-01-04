import threading
import time
import os
import sys
import fnmatch
import psutil
from datetime import datetime


class ProcessRun(object):
    def __init__(self):
        self.Body = ""
        self.Path = ""


class ThreadingExample(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """
    ProcessRun = object

    def __init__(self, ProcessRun, interval=5):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        self.ProcessRun = ProcessRun

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something

            print('Star command that ' +
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            try:
                funcs = {}
                exec(self.ProcessRun.Body, {}, funcs)
                for name in funcs:
                    if name == "run":
                        dd = funcs[name]
                        varrr = dd()

            except:
                e = sys.exc_info()[0]
                print("Ocurrio un error al ejecutar el archivo " +
                      self.ProcessRun.Path)

            print('End command that ' +
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            time.sleep(self.interval)


def Precess():
    ProcessRuns = []
    listOfFiles = os.listdir(os.path.join(os.getcwd(), "process"))
    pattern = "*.py"
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            print(entry)
            item = ProcessRun()
            filePath = os.path.join(
                os.getcwd(), "process",  entry)
            item.Body = open(filePath, "r").read()
            item.Path = filePath
            ProcessRuns.append(item)
    return ProcessRuns


process = Precess()
for item in process:
    example = ThreadingExample(item, 5)
time.sleep(5000)
print('Finished process')
