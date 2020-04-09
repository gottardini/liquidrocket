import config
from solver import Solver



if __name__=="__main__":
    data=config.getData(0)
    outputs=config.getOutputs()
    slvr=Solver(data,outputs)
    slvr.validateTree()
