import matplotlib.pyplot as plt
from collections import OrderedDict
import numpy as np

xs=[
    'x_conv',
    'x_div_plus',
    'x_div_minus',
]
ys=[
    'y_conv',
    'y_div_plus',
    'y_div_minus'
]

class NozzlePlotter:
    def __init__(self,rockets):
        self.rockets=rockets

    def make(self):
        engines=OrderedDict()
        for rocketName,rocketData in self.rockets.items():
            for blockIndex in range(len(rocketData)):
                block=rocketData[blockIndex]
                engName=block['engName']
                if engName in engines or block['type']!='liquid':
                    continue
                else:
                    engines[engName]=[]
                    for i in range(len(xs)):
                        engines[engName].append((block['solvedData'][xs[i]].getValue(),block['solvedData'][ys[i]].getValue()))

        for engName,engData in engines.items():
            fig, ax = plt.subplots(figsize=(10, 10),num=engName)
            ax.set_xlabel("m")
            ax.set_ylabel("m")
            ax.set_aspect('equal')
            ax.set_title(engName)
            ax.grid()
            for plot in engData:
                ax.plot(plot[1],-plot[0],color='black')
                ax.plot(-plot[1],-plot[0],color='black')
            fig.savefig('out/nozzles/'+engName.replace(" ","_")+".png",dpi=fig.dpi)
