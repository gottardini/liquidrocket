import matplotlib.pyplot as plt
from collections import OrderedDict
import numpy as np

class PostProcesser:
    def __init__(self):
        self.figures=OrderedDict({
            "Pressione in funzione della quota":['z',['p','p_tropo','p_e']],
            "Spinta in funzione della pressione":['p',['thr_var','thr_n','thr_ad']],
            "Spinta in funzione della quota":['z',['thr_var','thr_n','thr_ad']],
            })

        self.styles=[
            [{"color":"black"},{"color":"gray"},{"color":"green","linestyle":"--"}],
            [{"color":"blue"},{"color":"gray","linestyle":"--"},{"color":"green","linestyle":"--"}],
            [{"color":"blue"},{"color":"gray","linestyle":"--"},{"color":"green","linestyle":"--"}],
        ]

        self.markers=[
            [{"data":"z_ad","params":{"color":"gray","linestyle":"--","linewidth":1}}],
            [{"data":"p_e","params":{"color":"gray","linestyle":"--","linewidth":1}}],
            [{"data":"z_ad","params":{"color":"gray","linestyle":"--","linewidth":1}}],
        ]

        self.ticks=[

        ]

    def make(self,data):
        figures=list(self.figures.items())
        for index in range(len(figures)):
            figname=figures[index][0]
            dat=figures[index][1]
            fig,ax=plt.subplots(figsize=(8, 8),num=figname)
            xdata=data[dat[0]].getValue()
            ydatam=[]
            ax.set_xlabel(data[dat[0]].description)
            ax.set_ylabel(data[dat[1][0]].description)
            for jndex in range(len(dat[1])):
                ydata=data[dat[1][jndex]].getValue()
                #print(ydata)
                if len(ydata)!=len(xdata):
                    if len(ydata)==1:
                        ydata=np.full(len(xdata),ydata)
                style=self.styles[index][jndex]
                if style!=None:
                    ax.plot(xdata,ydata,label=data[dat[1][jndex]].description,**style)
                else:
                    ax.plot(xdata,ydata)
            markers=self.markers[index]
            if markers!=None:
                for marker in markers:
                    ax.axvline(data[marker["data"]].getValue(),0,1,label=data[marker["data"]].description,**marker["params"])
            ax.legend()
