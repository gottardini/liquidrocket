class Node:
    def __init__(self,variable):
        pass


class Variable:
    def __init__(self,description,value=None,calcFunction=None):
        self.description=description
        self.calcFunction=calcFunction
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
        params=[values[key] for key in bindings]
        return self.fun(*params)
