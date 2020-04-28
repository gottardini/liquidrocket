def make(self):

    ###GRAFICI
    figures=list(self.figures.items())
    for index in range(len(figures)):
        figname=figures[index][0]
        dat=figures[index][1]
        fig,ax=plt.subplots(figsize=(8, 8),num=figname)
        xdata=data[dat[0]].getValue()
        ydatam=[]
        ax.set_xlabel(self.labels[index][0])
        ax.set_ylabel(self.labels[index][1])
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
