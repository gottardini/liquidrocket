import config
from solver import Solver
from grapher import Grapher
import time
import matplotlib.pyplot as plt


if __name__=="__main__":
    outputs=config.getOutputs()
    data=config.getData(0)
    grph=Grapher()
    try:
        slvr=Solver(data,outputs,grph)
        slvr.validateTree()
    except:
        pass
    plt.show()
