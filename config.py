from loader import *
from source import *
"""
JUST
USE
S.I.
UNITS
PLS
"""

dataloader=DataLoader("source/data.csv")
inputData=dataloader.load()

#####################


def mergeData(sources):
    merged={}
    for elem in sources:
        merged={**merged,**elem}
    return merged

def getData(chosenEngine):
    if type(chosenEngine)==int:
        inputD=list(inputData.items())[chosenEngine][1]
    elif type(chosenEngine)==str:
        inputD=inputData[chosenEngine]
    else:
        raise ValueError("Invalid engine selection")
    sources=[constants,inputD,variables]
    return mergeData(sources)

def getOutputs():
    return outputs
