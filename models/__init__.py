import numpy as np
import collections
from rocketcea.cea_obj_w_units import CEA_Obj

class Node:
    def __init__(self,variable):
        pass


class Variable:
    #def __str__(self):
    #    return str(self.getValue())

    def __repr__(self):
        return str(self.getValue())

    def __init__(self,description,units,value,calcFunction):
        self.description=description
        self.units=units
        self.calcFunction=calcFunction
        if type(value)!=np.array:
            if type(value)==str:
                pass
            elif isinstance(value,collections.Iterable):
                value=np.array(value)
            else:
                value=np.array([value])
        self.value=value

    def getDependencies(self):
        if self.calcFunction is not None:
            return self.calcFunction.bindings
        else:
            return None

    def getCalcFunction(self):
        return self.calcFunction

    def getValue(self):
        return self.value

    def getReadableValue(self):
        if isinstance(self.value,np.ndarray):
            return np.array2string(self.value,edgeitems=2,threshold=3,precision=4)
        else:
            return str(self.value)

    def setValue(self,val):
        self.value=val

class InputVariable(Variable):
    def __init__(self,description,units,value):
        super().__init__(description,units,value,None)

class UnknownVariable(Variable):
    def __init__(self,description,units,calcFunction):
        super().__init__(description,units,None,calcFunction)


class CalcFunction:
    def __init__(self, fun, *bindings, iter=False):
        self.fun=fun
        self.bindings=bindings
        self.manualIter=iter

    def execute(self,values): #values is represented with a dictionary e.g. {"g":9.81}
        if not self.manualIter:
            params=[values[key] for key in self.bindings]
            res = self.fun(*params)
            if type(res)!=np.ndarray:
                if isinstance(res,CEA_Obj):
                    pass
                elif isinstance(res,list):
                    res=np.array(res)
                else:
                    res=np.array([res])
            return res
        else:
            res=np.array([])
            #lens=[len(values[key]) for key in self.bindings]
            lens=[]
            for key in self.bindings:
                val=values[key]
                if isinstance(val,np.ndarray) or isinstance(val,list):
                    lens.append(len(val))
                else:
                    lens.append(1)

            for i in range(np.amax(lens)):
                params=[]
                for j in range(len(self.bindings)):
                    val=values[self.bindings[j]]
                    if lens[j]>1:
                        params.append(val[i])
                    else:
                        if isinstance(val,np.ndarray):
                            params.append(val[0])
                        else:
                            params.append(val)
                res=np.append(res,self.fun(*params))
            return res
