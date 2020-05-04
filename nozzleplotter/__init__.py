import matplotlib.pyplot as plt
from collections import OrderedDict
import numpy as np

xs=[
    'x_cc',
    'x_rac',
    'x_conv',
    'x_div_plus',
    'x_div_minus',
]
ys=[
    'y_cc',
    'y_rac',
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

        engines=OrderedDict(sorted(engines.items(), key=lambda x: x[1][-1][0][-1]-x[1][0][0][0],reverse=True))

        compFig=plt.figure(figsize=(20, 8),num="Confronto motori")
        compAx=compFig.add_axes([0.06,0.05,0.9,0.9])
        compAx.set_axis_off()
        compAx.set_aspect('equal')

        #print(engines)
        cursor=0
        for engName,engData in engines.items():
            fig= plt.figure(figsize=(7, 10),num=engName)
            ax= fig.add_axes([0.06,0.05,0.9,0.9])
            ax.set_xlabel("m")
            ax.set_ylabel("m")
            ax.set_aspect('equal')
            #ax.set_title(engName)
            ax.grid()
            ax.plot([engData[0][1][-1],-engData[0][1][-1]],[-engData[0][0][-1],-engData[0][0][-1]],linestyle="--",color="orange")
            ax.plot([engData[2][1][-1],-engData[2][1][-1]],[-engData[2][0][-1],-engData[2][0][-1]],linestyle="--",color="gray")


            diam=engData[-1][1][-1]*2
            bellLength=engData[-1][0][-1]-engData[-2][0][0]
            totLength=engData[-1][0][-1]-engData[0][0][0]

            for plot in engData:
                ax.plot(plot[1],-plot[0],color='black')
                ax.plot(-plot[1],-plot[0],color='black')

                compAx.plot(plot[1]+cursor+diam/2,-plot[0]+bellLength,color='black')
                compAx.plot(-plot[1]+cursor+diam/2,-plot[0]+bellLength,color='black')
                compAx.text(cursor+diam/2,totLength+0.2,engName,horizontalalignment='center',verticalalignment='center',fontsize=16)
            fig.savefig('out/nozzles/'+engName.replace(" ","_")+".png",dpi=fig.dpi)
            cursor+=diam+0.4
        compFig.savefig('out/nozzles/compare.svg')
