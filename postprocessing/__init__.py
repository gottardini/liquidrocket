import matplotlib.pyplot as plt
from collections import OrderedDict
import numpy as np

class PostProcesser:
    def __init__(self,rockets):
        self.rockets=rockets

        self.rocketColors=['#cc3300','#009900','#003399']
        self.stageColors=['#6600cc','#997300','#008060','black']
        self.stageStyles=['-','--','-.',':']
        self.adColors=['#222222','#555555','#777777','#999999',]


    ###THIS IS ABOUT TO GET MESSY AND NOT FLEXIBLE, BUT I HAVE NO TIME TO MAKE IT BTFL
    def make(self):
        ###THRUST-Z
        figThrust_z, axThrust_z = plt.subplots(figsize=(12, 8),num="Spinta in funzione della quota")
        axThrust_z.set_xlabel("Quota [m]")
        axThrust_z.set_ylabel("Spinta [N]")
        axThrust_z.set_title("Spinta in funzione della quota")
        axThrust_z.set_yscale('linear')
        axThrust_z.grid(True, which="both")

        ###ISP-Z
        figIsp_z, axIsp_z = plt.subplots(figsize=(12, 8),num="Impulso specifico in funzione della quota")
        axIsp_z.set_xlabel("Quota [m]")
        axIsp_z.set_ylabel("Impulso specifico [s]")
        axIsp_z.set_title("Impulso specifico in funzione della quota")
        axIsp_z.set_yscale('linear')
        axIsp_z.grid(True, which="both")

        ###CT-Z
        figCt_z, axCt_z = plt.subplots(figsize=(12, 8),num="Coefficiente di spinta in funzione della quota")
        axCt_z.set_xlabel("Quota [m]")
        axCt_z.set_ylabel("Coefficiente di spinta [-]")
        axCt_z.set_title("Coefficiente di spinta in funzione della quota")
        axCt_z.set_yscale('linear')
        axCt_z.grid(True, which="both")

        i=0
        for rocketName, rocket in self.rockets.items():
            ###SEP THRUST-Z
            sep_figThrust_z, sep_axThrust_z = plt.subplots(figsize=(12, 8),num="Spinta in funzione della quota - %s"%(rocketName))
            sep_axThrust_z.set_xlabel("Quota [m]")
            sep_axThrust_z.set_ylabel("Spinta [N]")
            sep_axThrust_z.set_title("Spinta in funzione della quota - %s"%(rocketName))
            sep_axThrust_z.set_yscale('linear')
            sep_axThrust_z.grid(True, which="both")

            ###SEP ISP-Z
            sep_figIsp_z, sep_axIsp_z = plt.subplots(figsize=(12, 8),num="Impulso specifico in funzione della quota- %s"%(rocketName))
            sep_axIsp_z.set_xlabel("Quota [m]")
            sep_axIsp_z.set_ylabel("Impulso specifico [s]")
            sep_axIsp_z.set_title("Impulso specifico in funzione della quota - %s"%(rocketName))
            sep_axIsp_z.set_yscale('linear')
            sep_axIsp_z.grid(True, which="both")

            ###SEP CT-Z
            sep_figCt_z, sep_axCt_z = plt.subplots(figsize=(12, 8),num="Coefficiente di spinta in funzione della quota- %s"%(rocketName))
            sep_axCt_z.set_xlabel("Quota [m]")
            sep_axCt_z.set_ylabel("Coefficiente di spinta [-]")
            sep_axCt_z.set_title("Coefficiente di spinta in funzione della quota- %s"%(rocketName))
            sep_axCt_z.set_yscale('linear')
            sep_axCt_z.grid(True, which="both")

            for blockIndex in range(len(rocket)):
                block=rocket[blockIndex]
                blockSolved=block['solvedData']

                ###THRUST-Z
                sep_axThrust_z.plot(blockSolved['z'].getValue(),blockSolved['thr_var'].getValue()*block['qty'],label=block['name'],color=self.stageColors[blockIndex])
                axThrust_z.plot(blockSolved['z'].getValue(),blockSolved['thr_var'].getValue()*block['qty'],label="%s - %s"%(rocketName,block['name']),color=self.rocketColors[i],linestyle=self.stageStyles[blockIndex])
                if (blockIndex==0 or False) and block['type']=='liquid':
                    sep_axThrust_z.axvline(blockSolved['z_ad'].getValue(),0,1,label="Quota di adattamento - %s"%(block['name']),linestyle="--",color=self.adColors[blockIndex])

                ###ISP-Z
                sep_axIsp_z.plot(blockSolved['z'].getValue(),blockSolved['I_s'].getValue(),label=block['name'],color=self.stageColors[blockIndex])
                axIsp_z.plot(blockSolved['z'].getValue(),blockSolved['I_s'].getValue(),label="%s - %s"%(rocketName,block['name']),color=self.rocketColors[i],linestyle=self.stageStyles[blockIndex])

                if block['type']=='liquid':
                    ###CT-Z
                    sep_axCt_z.plot(blockSolved['z'].getValue(),blockSolved['ct_var'].getValue(),label=block['name'],color=self.stageColors[blockIndex])
                    axCt_z.plot(blockSolved['z'].getValue(),blockSolved['ct_var'].getValue(),label="%s - %s"%(rocketName,block['name']),color=self.rocketColors[i],linestyle=self.stageStyles[blockIndex])

            sep_axThrust_z.legend()
            sep_figThrust_z.savefig('out/performance/single/'+("Spinta-Quota %s"%(rocketName)).replace(" ","_")+".svg")

            sep_axIsp_z.legend()
            sep_figIsp_z.savefig('out/performance/single/'+("Isp-Quota %s"%(rocketName)).replace(" ","_")+".svg")

            sep_axCt_z.legend()
            sep_figCt_z.savefig('out/performance/single/'+("Ct-Quota %s"%(rocketName)).replace(" ","_")+".svg")

            i+=1

        axThrust_z.legend()
        figThrust_z.savefig('out/performance/multi/'+"Spinta-Quota.svg")

        axIsp_z.legend()
        figIsp_z.savefig('out/performance/multi/'+"Isp-Quota.svg")

        axCt_z.legend()
        figCt_z.savefig('out/performance/multi/'+"Ct-Quota.svg")
