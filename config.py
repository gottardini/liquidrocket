from models import *
from functions import *
from loader import *
"""
JUST
USE
S.I.
UNITS
PLS
"""

dataloader=DataLoader("loader/data.csv")
inputData=dataloader.load()

constants={
    "R_u":InputVariable("Ideal gas constant [J/(mol*K)]", 8.31446261815324),
    "g_o":InputVariable("Gravitational acceleration at zero altitude [m/s^2]", 9.807),
    "a":InputVariable("Vertical temperature gradient [K/m]",0.0065),
    "p_0":InputVariable("Pressure at zero altitude [Pa]", 101325),
    "T_0":InputVariable("Temperature at zero altitude [K]", 288.16)
}

###ACTUAL "SCRIPTING"
variables={
    "R_cp":UnknownVariable("Exhaust gases constant",CalcFunction(calcGasConstant,'R_u','Mm_cp')),
    "GAMMA":UnknownVariable("Van Kerckhove function",CalcFunction(vanker,'y_b'))
}

outputs=["R_cp"]
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
