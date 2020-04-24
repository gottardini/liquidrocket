import numpy as np
import collections

class Node:
    def __init__(self,variable):
        pass


class Variable:
    def __str__(self):
        return self.getValue()

    def __repr__(self):
        return str(self.getValue())

    def __init__(self,description,value=None,calcFunction=None):
        self.description=description
        self.calcFunction=calcFunction
        if type(value)!=np.array:
            if type(value)==str:
                pass
            elif isinstance(value,collections.Iterable):
                value=np.array(value)
            #else:
            #    value=np.array([value])
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

    def setValue(self,val):
        self.value=val

class InputVariable(Variable):
    def __init__(self,description,value):
        super().__init__(description,value,None)

class UnknownVariable(Variable):
    def __init__(self,description,calcFunction):
        super().__init__(description,None,calcFunction)


class CalcFunction:
    def __init__(self, fun, *bindings):
        self.fun=fun
        self.bindings=bindings

    def execute(self,values): #values is represented with a dictionary e.g. {"g":9.81}
        params=[values[key] for key in self.bindings]
        return self.fun(*params)
