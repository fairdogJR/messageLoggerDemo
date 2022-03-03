# read log file

import glob
import os
from datetime import *


def getErrorinfo(logfileDir):
    global line
    # get newest file in log dir
    #logfileDir = r'C:\Users\fairfiel.KEYSIGHT\AppData\Local\Keysight\M8070B'
    list_of_files = glob.glob(logfileDir + '\*.txt')  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)
    latestLogFile = open(latest_file, 'r')
    Lines = latestLogFile.readlines()
    errorList = []
    count = 0
    errcount=0
    # look for "Error" in column 2
    for line in Lines:
        count += 1
        if "Error" in line:
            #     print("Line{}: {}".format(count, line.strip()))
            findError = line.split()
            if findError[1] == "Error":
                #print("Line{}: {}".format(count, line.strip()))
                errorList.append(line.strip())
                errcount+=1
    # print all errors seen if any
    if errcount > 0:
        print("------logfile error list-----")
        print(errorList)
        for each in errorList:
            print(each)
        # print present time
        tdate = datetime.now();
        temp2 = errorList[-1].split("\t")
        lastErrorTime = temp2[0].split("-")
        # print (presentDatetime)
        print("time now", tdate)
        print(f"{errcount} total errors found")
        #print("last error time", lastErrorTime)
        # print the last error seen if any
        print("last error: ", errorList[-1])
        # datetime_objectcompare = datetime.strptime(presentDatetime[1],'%H:%M:%S.%f')
        lastErrorTime2 = lastErrorTime[0] + " " + lastErrorTime[1]
        datetimeLastError = datetime.strptime(lastErrorTime2, '%Y.%m.%d %H:%M:%S.%f')
        diff = tdate - datetimeLastError
        # print("time since last error=", diff)
        minutes = divmod(diff.total_seconds(), 60)
        print(f"{minutes[0]} minutes since last error")
    else:
        print("no error info")


getErrorinfo(r'C:\Users\fairfiel.KEYSIGHT\AppData\Local\Keysight\M8070B')
