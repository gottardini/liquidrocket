import config
import source
import loader as ld
import logging
import time


def mergeData(sources):
    merged={}
    for elem in sources:
        for key,val in elem.items():
            if key in merged:
                raise ValueError("Dupilcate found")
                return False
            else:
                merged[key]=val
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
    #print(inputData)
    #######
    sources=[getEngineData(inputData,chosenEngine)]
    for varname in dir(source):
        varblock=getattr(source,varname)
        if not varname.startswith("__") and type(varblock)==dict:
            sources.append(varblock)
    #######

    return mergeData(sources)

def getOutputs():
    return list(filter(lambda x: x!='',open(config.jobfile).read().split("\n")))

def getPostProc():
    return list(filter(lambda x: x!='',open(config.postprocfile).read().split("\n")))

def getLogo():
    return open("utils/logo.txt").read()

def tic():
    #Homemade version of matlab tic and toc functions
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    if 'startTime_for_tictoc' in globals():
        return time.time() - startTime_for_tictoc
