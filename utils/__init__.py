import config
import source
import loader as ld
import logging
import time


def mergeData(sources):
    merged={}
    for elem in sources:
        merged={**merged,**elem}
    return merged

def getEngineData(inputData,chosenEngine):
    if type(chosenEngine)==int:
        inputD=list(inputData.items())[chosenEngine][1]
    elif type(chosenEngine)==str:
        inputD=inputData[chosenEngine]
    else:
        raise ValueError("Invalid engine selection")

    return inputD

def getData(chosenEngine):
    loader=ld.DataLoader(config.datafile)
    inputData=loader.load()

    #######
    sources=[source.constants,source.variables,getEngineData(inputData,chosenEngine)]
    #######

    return mergeData(sources)

def getOutputs():
    return open(config.jobfile).read()[:-1].split("\n")

def getLogo():
    return open("utils/logo.txt").read()

def tic():
    #Homemade version of matlab tic and toc functions
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    if 'startTime_for_tictoc' in globals():
        return time.time() - startTime_for_tictoc
