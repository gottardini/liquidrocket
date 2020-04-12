from collections import OrderedDict

class Solver:
    def __init__(self,data,outputs,grph,logger):
        self.data=data
        self.dataKeySet=set(self.data.keys())
        self.outputs=outputs
        self.outKeys=set(self.outputs)
        self.visited=[]
        self.grapher=grph
        self.logger=logger

    def solve(self):
        result=OrderedDict()
        self.logger.debug("Starting solver")
        for out in self.outputs:
            self.logger.debug("Starting branch from node '%s'"%(out))
            if not self.solveRecursively(out):
                self.logger.error("Branch started from node '%s' has encountered an error"%(out))
                return False
            self.logger.debug("Branch started from node '%s' solved successfully"%(out))
            result[out]=self.data[out].getValue()
        self.logger.debug("Solving concluded successfully")
        self.grapher.drawGraph()
        return result


    def solveRecursively(self,nodename):
        self.logger.debug("Solver is currently at node '%s'"%(nodename))
        if self.data[nodename].getValue() is not None:
            self.logger.debug("Node '%s' has a value. Branch dies here"%(nodename))
            self.grapher.changeNodeColor(nodename,'#8DFF33')
            return
        calcFunction=self.data[nodename].getCalcFunction()
        dependencies=self.data[nodename].getDependencies()
        if dependencies is None:
            self.logger.critical("Something's wrong with node '%s', has no value nor dependencies"%(nodename))
            return False
        self.logger.debug("Node '%s' has %s dependencies, digging into them"%(nodename,len(dependencies)))
        for dep in dependencies:
            self.solveRecursively(dep)
        self.logger.debug("Dependencies for node '%s' are satisfied. gathering them..."%(nodename))
        args={dep:self.data[dep].getValue() for dep in dependencies}
        #At this point each dependency has a value, so we can calculate the current nodes
        self.logger.debug("Evaluating node '%s'"%(nodename))
        self.data[nodename].setValue(calcFunction.execute(args))
        self.logger.debug("Node '%s' successfully evaluated. Proceeding..."%(nodename))
        self.grapher.changeNodeColor(nodename,'#8DFF33')
        return True



    def validateTree(self):
        if len(self.outKeys)!=len(self.outputs):
            self.logger.error("There are duplicates in the requested outputs")
            return False
        self.visited=[]
        for out in self.outputs:
            self.grapher.addNode(out,out,None)
            self.grapher.changeNodeColor(out,'#C70039')

        if all([self.validateNodeRecursively(out,[out]) for out in self.outputs]):
            self.logger.info("Valid tree")
            self.grapher.drawGraph()
            return True
        return False


    def validateNodeRecursively(self,nodename,localvisited):
        self.logger.debug("Visiting node '%s'"%(nodename))
        if nodename in self.visited:
            self.logger.debug("Node '%s' already visited. Going on..."%nodename)
            return True
        else:
            #Check if the current node exists (actually required just for the output nodes)
            if nodename not in self.data:
                self.logger.critical("Couldn't find node '%s'"%(nodename))
                return False
            self.visited.append(nodename)
            dependencies=self.data[nodename].getDependencies()
            if dependencies is not None:
                self.logger.debug("Node '%s' has %s depencencies. Visiting them..."%(nodename,len(dependencies)))
                dependenciesSet=set(dependencies)
                keysInter=dependenciesSet.intersection(self.dataKeySet)
                missing=dependenciesSet.difference(keysInter)
                if len(missing):
                    self.logger.critical("Couldn't resolve the following dependencies for node '%s':\n\n%s"%(nodename,'\n'.join(list(missing))))
                    return False

                for dep in dependencies:
                    if dep in localvisited:
                        logger.critical("Loop detected with nodes '%s' and '%s'"%(nodename,dep))
                        return False
                    self.grapher.addNode(dep,dep,nodename)
                    if dep not in self.visited:
                        self.grapher.changeNodeColor(dep,'#C70039')
                    #input(".")
                if all([self.validateNodeRecursively(dep,localvisited[:]+[dep]) for dep in dependencies]):
                    self.grapher.changeNodeColor(nodename,'#F9FF33')
                    return True
            else:
                self.logger.debug("Node '%s' has no dependencies, fine!")
                self.grapher.changeNodeColor(nodename,'#F9FF33')
                return True
