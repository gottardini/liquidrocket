import matplotlib.pyplot as plt
import config
from loader import DataLoader
from collections import OrderedDict
import numpy as np


class Comparer:
    def __init__(self,rockets):
        self.rockets=rockets
        loader=DataLoader('comparer/barplots.csv')
        self.data=loader.load()
        self.vars=list(self.data.items())[0][1]
        self.plots=list(self.vars.keys())
        #print(self.plots)

    def autolabel(self,rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    def make(self):
        for plotIndex in range(len(self.plots)):
            varname=self.plots[plotIndex]
            var=self.vars[varname]
            fig= plt.figure(figsize=(12, 6),num=var.description)
            ax= fig.add_axes([0.06,0.05,0.9,0.9])
            ax.set_ylabel(var.units)
            #ax.set_title(var.description)
            #ax.grid()
            engines=OrderedDict()
            for rocketName,rocketData in self.rockets.items():
                for blockIndex in range(len(rocketData)):
                    block=rocketData[blockIndex]
                    engName=block['engName']
                    if engName in engines or block['type']!='liquid':
                        continue
                    else:
                        realValue=self.data[engName][varname].getValue()
                        calcValue=block['solvedData'][varname].getValue()
                        engines[engName]=(realValue,calcValue)
            labels=list(engines.keys())
            real=[v[0] for x,v in engines.items()]
            calc=[v[1] for x,v in engines.items()]
            real=[0 if x[0] is None else x[0] for x in real]
            calc=[0 if x[0] is None else x[0] for x in calc]

            x = np.arange(len(labels))  # the label locations
            width = 0.35  # the width of the bars

            rects1 = ax.bar(x - width/2, real, width, label='Valore reale',)
            rects2 = ax.bar(x + width/2, calc, width, label='Valore calcolato',)

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax.set_xticks(x)
            ax.set_xticklabels(labels)
            ax.legend()
            fig.savefig('out/comparer/'+var.description.replace(" ","_")+".png",dpi=fig.dpi)
