import csv
from models import *
from collections import OrderedDict
#settings
symbolCol=1
nameCol=0
firstEngineCol=3

class DataLoader:
    def __init__(self,path):
        self.path=path

    def load(self):
        file=open(self.path)
        reader=csv.reader(file)
        data=[row for row in reader]
        nEngines=len(data[0])-firstEngineCol
        engines=OrderedDict()
        for i in range(nEngines):
            engines[data[0][firstEngineCol+i]]={}
        for row in data[1:]:
            #print(row)
            for i in range(nEngines):
                rawval=row[firstEngineCol+i]
                try:
                    val=float(rawval)
                except:
                    if rawval!='':
                        val=rawval
                    else:
                        val=None
                engines[data[0][firstEngineCol+i]][row[symbolCol]]=InputVariable(row[nameCol],val)
        return engines
