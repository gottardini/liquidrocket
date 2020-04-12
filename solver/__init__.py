from collections import OrderedDict

class Solver:
    def __init__(self,data,outputs,grph):
        self.data=data
        self.dataKeySet=set(self.data.keys())
        self.outputs=outputs
        self.outKeys=set(self.outputs)
        self.visited=[]
        self.grapher=grph

    def solve(self):
        result=OrderedDict()
        for out in self.outputs:
            self.solveRecursively(out)
            result[out]=self.data[out].getValue()
        self.grapher.drawGraph()
        return result


    def solveRecursively(self,nodename):
        if self.data[nodename].getValue() is not None:
            self.grapher.changeNodeColor(nodename,'#8DFF33')
            return
        calcFunction=self.data[nodename].getCalcFunction()
        dependencies=self.data[nodename].getDependencies()
        if dependencies is None:
            raise ValueError("Something's wrong with node '%s', has no value nor dependencies"%(nodename))
        for dep in dependencies:
            self.solveRecursively(dep)
        args={dep:self.data[dep].getValue() for dep in dependencies}
        #At this point each dependency has a value, so we can calculate the current nodes
        self.data[nodename].setValue(calcFunction.execute(args))
        self.grapher.changeNodeColor(nodename,'#8DFF33')
        return



    def validateTree(self):
        if len(self.outKeys)!=len(self.outputs):
            raise ValueError("There are duplicates in the requested outputs")
        self.visited=[]
        for out in self.outputs:
            self.grapher.addNode(out,out,None)
            self.grapher.changeNodeColor(out,'#C70039')

        if all([self.validateNodeRecursively(out,[out]) for out in self.outputs]):
            print("Valid tree")
            self.grapher.drawGraph()
            return True
        return False


    def validateNodeRecursively(self,nodename,localvisited):
        #print("Visiting node",nodename)
        if nodename in self.visited:
            return True
        else:
            #Check if the current node exists (actually required just for the output nodes)
            if nodename not in self.data:
                raise ValueError("Couldn't find node '%s'"%(nodename))
            self.visited.append(nodename)
            dependencies=self.data[nodename].getDependencies()
            if dependencies is not None:
                dependenciesSet=set(dependencies)
                keysInter=dependenciesSet.intersection(self.dataKeySet)
                missing=dependenciesSet.difference(keysInter)
                if len(missing):
                    raise ValueError("Couldn't resolve the following dependencies for node '%s':\n\n%s"%(nodename,'\n'.join(list(missing))))

                for dep in dependencies:
                    if dep in localvisited:
                        raise ValueError("Loop detected with nodes '%s' and '%s'"%(nodename,dep))
                    self.grapher.addNode(dep,dep,nodename)
                    if dep not in self.visited:
                        self.grapher.changeNodeColor(dep,'#C70039')
                    #input(".")
                if all([self.validateNodeRecursively(dep,localvisited[:]+[dep]) for dep in dependencies]):
                    self.grapher.changeNodeColor(nodename,'#F9FF33')
                    return True
            else:
                self.grapher.changeNodeColor(nodename,'#F9FF33')
                return True
