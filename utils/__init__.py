import config
import source
import source.solid as source_solid
import loader as ld
import logging
import time
from models import UnknownVariable, InputVariable, Variable

def formatData(data, inputData, task):
    out="\n   {:<15}{:<60}{:<20}{:<60}\n".format("Simbolo", "Descrizione", "Unità di misura","Valore")

    out+="\nINPUT_DATA\n"
    for _varname,_vardata in inputData.items():
        out+= "   {:<15}{:<60}{:<20}{:<60}\n".format(_varname, _vardata.description,inputData[_varname].units, inputData[_varname].getReadableValue())

    for varname in dir(source):
        varblock=getattr(source,varname)
        if not varname.startswith("__") and type(varblock)==dict:
            out+="\n>"+varname.upper()+"\n"
            for _varname,_vardata in varblock.items():
                if isinstance(_vardata,InputVariable) or (isinstance(_vardata,UnknownVariable) and _varname in task):
                    out+= "   {:<15}{:<60}{:<20}{:<60}\n".format(_varname, _vardata.description,data[_varname].units, data[_varname].getReadableValue())
    return out

def mergeData(sources):
    merged={}
    for elem in sources:
        for key,val in elem.items():
            if key in merged:
                raise ValueError("Dupilcate found: %s"%(key))
                return False
            else:
                merged[key]=val
    return merged

def getEngineData(inputData,chosenEngine):
    if type(chosenEngine)==int:
        engineName,inputD=list(inputData.items())[chosenEngine]
    elif type(chosenEngine)==str:
        engineName=chosenEngine
        inputD=inputData[chosenEngine]
    else:
        raise ValueError("Invalid engine selection")
    return engineName,inputD

def getInputData():
    loader=ld.DataLoader(config.datafile)
    return loader.load()

def getUnsolvedModel(typ):
    sources=[]
    varlist=dir(source if typ=='liquid' else source_solid)
    print(varlist)
    for varname in varlist:
        varblock=getattr(source,varname)
        if not varname.startswith("__") and type(varblock)==dict:
            sources.append(varblock)
    return mergeData(sources).copy()

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
