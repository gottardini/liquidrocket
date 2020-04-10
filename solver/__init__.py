class Solver:
    def __init__(self,data,outputs,grph):
        self.data=data
        self.dataKeySet=set(self.data.keys())
        self.outputs=outputs
        self.visited=[]
        self.grapher=grph

    def validateTree(self):
        outKeys=set(self.outputs)
        if len(outKeys)!=len(self.outputs):
            raise ValueError("There are duplicates in the requested outputs")
        self.visited=[]
        for out in self.outputs:
            self.grapher.addNode(out,out,None)

        if all([self.validateNodeRecursively(out,[out]) for out in self.outputs]):
            print("Valid tree")


    def validateNodeRecursively(self,nodename,localvisited):
        print("Visiting node",nodename)
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
                    self.grapher.pause(0.01)
                if all([self.validateNodeRecursively(dep,localvisited[:]+[dep]) for dep in dependencies]):
                    return True
            else:
                return True
